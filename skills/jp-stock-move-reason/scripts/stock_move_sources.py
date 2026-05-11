#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collect local evidence for Codex to analyze a Japanese stock move.

This intentionally does not call Gemini or any other LLM. It reuses the shape of
the /pts scraper: Yahoo! Finance forum comments, stock news, and basic metrics
are collected, then printed as a compact evidence brief for Codex to analyze.
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import html
import io
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Any


JST = dt.timezone(dt.timedelta(hours=9), "JST")
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)
INFO_KEYWORDS = [
    "決算",
    "上方修正",
    "下方修正",
    "増配",
    "減配",
    "自社株買い",
    "株式分割",
    "提携",
    "資本提携",
    "業務提携",
    "受注",
    "承認",
    "認可",
    "特許",
    "IR",
    "黒字",
    "黒字化",
    "TOB",
    "MBO",
    "買収",
    "補助金",
    "採択",
    "契約",
    "大量保有",
    "新製品",
    "月次",
    "配当",
    "優待",
]


def now_jst() -> dt.datetime:
    return dt.datetime.now(JST).replace(tzinfo=None)


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<!--.*?-->", "", value, flags=re.DOTALL)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def normalize_symbol(raw: str) -> tuple[str, str]:
    raw = raw.strip().upper()
    if not raw:
        raise ValueError("stock code is empty")
    if "." in raw:
        code = raw.split(".", 1)[0]
        return code, raw
    if re.match(r"^\d{3}[0-9A-Z]$", raw):
        return raw, f"{raw}.T"
    return raw, raw


def yahoo_quote_url(symbol: str) -> str:
    return f"https://finance.yahoo.co.jp/quote/{urllib.parse.quote(symbol)}"


def yahoo_forum_url(symbol: str) -> str:
    return f"{yahoo_quote_url(symbol)}/forum"


def yahoo_news_url(symbol: str) -> str:
    return f"{yahoo_quote_url(symbol)}/news"


def get_traders_prefix(market_name: str) -> str:
    if any(x in market_name for x in ["東Ｅ", "東E", "東証E", "ETF", "ETN"]):
        return "00"
    if any(x in market_name for x in ["プライム", "東Ｐ", "東P", "東証P", "PRM"]):
        return "61"
    if any(x in market_name for x in ["スタンダード", "東Ｓ", "東S", "東証S", "STD"]):
        return "62"
    if any(x in market_name for x in ["グロース", "東Ｇ", "東G", "東証G", "GRT"]):
        return "63"
    return "61"


def fetch_url(url: str, referer: str | None = None, timeout: int = 20, pause: bool = True) -> str:
    if pause:
        time.sleep(random.uniform(0.5, 1.4))
    if not referer:
        if "finance.yahoo.co.jp" in url:
            referer = "https://finance.yahoo.co.jp/"
        elif "kabutan.jp" in url:
            referer = "https://kabutan.jp/"
        elif "traders.co.jp" in url:
            referer = "https://www.traders.co.jp/"
        else:
            referer = "https://www.google.com/"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Referer": referer,
            "Cache-Control": "max-age=0",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read()
        encoding = response.info().get("Content-Encoding", "")
        if encoding == "gzip":
            body = gzip.decompress(body)
        elif encoding == "deflate":
            import zlib

            body = zlib.decompress(body)
        return body.decode("utf-8", errors="ignore")


def parse_jst_datetime(date_str: str) -> dt.datetime | None:
    clean = re.sub(r"\([^)]+\)", "", str(date_str or ""))
    clean = re.sub(r"\s+", " ", clean).strip()
    current = now_jst()
    patterns = [
        (r"^(\d{4})/(\d{1,2})/(\d{1,2})\s+(\d{1,2}):(\d{1,2})", True),
        (r"^(\d{2})/(\d{1,2})/(\d{1,2})\s+(\d{1,2}):(\d{1,2})", True),
        (r"^(\d{1,2})/(\d{1,2})\s+(\d{1,2}):(\d{1,2})", False),
    ]
    for pattern, has_year in patterns:
        match = re.search(pattern, clean)
        if not match:
            continue
        try:
            if has_year:
                year_raw, month, day, hour, minute = [int(x) for x in match.groups()]
                year = year_raw if year_raw >= 100 else 2000 + year_raw
            else:
                month, day, hour, minute = [int(x) for x in match.groups()]
                year = current.year
            parsed = dt.datetime(year, month, day, hour, minute)
            if not has_year and parsed > current + dt.timedelta(days=1):
                parsed = parsed.replace(year=year - 1)
            return parsed
        except ValueError:
            continue
    return None


def within_hours(date_str: str, hours: int) -> bool:
    parsed = parse_jst_datetime(date_str)
    if not parsed:
        return True
    return now_jst() - dt.timedelta(hours=hours) <= parsed <= now_jst() + dt.timedelta(minutes=5)


def age_label(date_str: str) -> str:
    parsed = parse_jst_datetime(date_str)
    if not parsed:
        return ""
    hours = max(0.0, (now_jst() - parsed).total_seconds() / 3600)
    if hours < 1:
        return f"{int(hours * 60)}分前"
    if hours < 48:
        return f"{hours:.1f}時間前"
    return f"{hours / 24:.1f}日前"


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title = ""
        self.meta_description = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = {k: v or "" for k, v in attrs}
        if tag == "title":
            self.in_title = True
        if tag == "meta" and attrs_d.get("name") == "description":
            self.meta_description = attrs_d.get("content", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


class YahooBBSParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.comments: list[dict[str, Any]] = []
        self.in_article = False
        self.current_article_raw = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "article":
            self.in_article = True
            self.current_article_raw = ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "article":
            self.in_article = False
            self.process_article()

    def handle_data(self, data: str) -> None:
        if self.in_article:
            self.current_article_raw += data

    def process_article(self) -> None:
        full_text = clean_text(self.current_article_raw)
        if not full_text:
            return

        date_str = ""
        match_date = re.search(r"\d{4}/\d{1,2}/\d{1,2}\s+\d{1,2}:\d{1,2}", full_text)
        if match_date:
            date_str = match_date.group(0)

        likes = 0
        match_likes = re.search(r"投資の参考になりましたか.*?はい\s*(\d+)", full_text, re.DOTALL)
        if match_likes:
            likes = int(match_likes.group(1))

        body_text = full_text
        if date_str and date_str in body_text:
            body_text = body_text.split(date_str, 1)[-1]
        body_text = body_text.split("投資の参考になりましたか", 1)[0]
        body_text = re.sub(r"返信[\s.]*$", "", body_text).strip()

        for sentiment in ["強く売りたい", "売りたい", "様子見", "買いたい", "強く買いたい"]:
            if body_text.startswith(sentiment):
                body_text = body_text[len(sentiment) :].strip()
        body_text = re.sub(r"^No\.\d+\s*報告", "", body_text).strip()
        if body_text.startswith("報告"):
            body_text = body_text[2:].strip()

        if body_text:
            self.comments.append(
                {
                    "date": date_str,
                    "likes": likes,
                    "text": body_text[:420] + ("..." if len(body_text) > 420 else ""),
                }
            )


class KabutanNewsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.news: list[dict[str, str]] = []
        self.company_name = ""
        self.in_si_i1_1 = False
        self.in_h2 = False
        self.in_span = False
        self.in_table = False
        self.current_row: list[Any] = []
        self.in_td = False
        self.current_td_text = ""
        self.in_anchor = False
        self.current_anchor_text = ""
        self.current_anchor_href = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = {k: v or "" for k, v in attrs}
        if tag == "div" and "si_i1_1" in attrs_d.get("class", "").split():
            self.in_si_i1_1 = True
        if tag == "h2" and self.in_si_i1_1:
            self.in_h2 = True
        if tag == "span" and self.in_h2:
            self.in_span = True
        if tag == "table" and "s_news_list" in attrs_d.get("class", ""):
            self.in_table = True
        if self.in_table and tag == "tr":
            self.current_row = []
        if self.in_table and tag == "td":
            self.in_td = True
            self.current_td_text = ""
        if self.in_table and tag == "a" and self.in_td:
            self.in_anchor = True
            self.current_anchor_text = ""
            self.current_anchor_href = attrs_d.get("href", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2":
            self.in_h2 = False
        if tag == "span":
            self.in_span = False
        if tag == "a" and self.in_anchor:
            self.in_anchor = False
        if tag == "td" and self.in_table:
            self.in_td = False
            if self.current_anchor_href:
                self.current_row.append({"text": clean_text(self.current_anchor_text), "href": self.current_anchor_href})
                self.current_anchor_href = ""
                self.current_anchor_text = ""
            else:
                self.current_row.append(clean_text(self.current_td_text))
        if tag == "tr" and self.in_table:
            self.process_row()
            self.current_row = []
        if tag == "table":
            self.in_table = False

    def handle_data(self, data: str) -> None:
        if self.in_h2 and not self.in_span:
            self.company_name += data
        if self.in_anchor:
            self.current_anchor_text += data
        if self.in_td:
            self.current_td_text += data

    def process_row(self) -> None:
        if len(self.current_row) < 3 or not isinstance(self.current_row[2], dict):
            return
        date_txt = self.current_row[0].get("text", "") if isinstance(self.current_row[0], dict) else str(self.current_row[0])
        if not any(char.isdigit() for char in date_txt):
            return
        title_obj = self.current_row[2]
        link = title_obj.get("href", "")
        if link.startswith("/"):
            link = "https://kabutan.jp" + link
        title = clean_text(title_obj.get("text", ""))
        if title:
            self.news.append({"title": title, "link": link, "pubDate": clean_text(date_txt), "source": "Kabutan"})


class TradersNewsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.news: list[dict[str, str]] = []
        self.in_news_container = False
        self.in_anchor = False
        self.in_timestamp = False
        self.current_url = ""
        self.current_title = ""
        self.current_timestamp = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = {k: v or "" for k, v in attrs}
        classes = attrs_d.get("class", "").split()
        if tag == "div" and "news_container" in classes:
            self.in_news_container = True
        if self.in_news_container and tag == "a" and "news_link" in classes:
            self.in_anchor = True
            self.current_url = attrs_d.get("href", "")
            self.current_title = ""
        elif self.in_news_container and tag == "div" and "timestamp" in classes:
            self.in_timestamp = True
            self.current_timestamp = ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.in_anchor:
            self.in_anchor = False
        elif tag == "div" and self.in_timestamp:
            self.in_timestamp = False
        if self.current_title and self.current_timestamp and not self.in_anchor and not self.in_timestamp:
            link = self.current_url
            if link.startswith("/"):
                link = "https://www.traders.co.jp" + link
            elif link and not link.startswith("http"):
                link = "https://www.traders.co.jp/" + link
            self.news.append(
                {
                    "title": clean_text(self.current_title),
                    "link": link,
                    "pubDate": clean_text(self.current_timestamp),
                    "source": "TradersWeb",
                }
            )
            self.current_title = ""
            self.current_timestamp = ""
            self.current_url = ""

    def handle_data(self, data: str) -> None:
        if self.in_anchor:
            self.current_title += data
        elif self.in_timestamp:
            self.current_timestamp += data


class AnchorParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.anchors: list[dict[str, str]] = []
        self.in_anchor = False
        self.current_href = ""
        self.current_text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attrs_d = {k: v or "" for k, v in attrs}
        self.in_anchor = True
        self.current_href = attrs_d.get("href", "")
        self.current_text = attrs_d.get("aria-label", "") or attrs_d.get("title", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.in_anchor:
            text = clean_text(self.current_text)
            href = urllib.parse.urljoin(self.base_url, self.current_href)
            if text and href:
                self.anchors.append({"title": text, "link": href})
            self.in_anchor = False
            self.current_href = ""
            self.current_text = ""

    def handle_data(self, data: str) -> None:
        if self.in_anchor:
            self.current_text += data


class TradersQuoteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.metrics = {
            "market_cap": "",
            "per": "",
            "pbr": "",
            "dividend_yield": "",
            "credit_buy": "",
            "credit_sell": "",
            "credit_ratio": "",
            "previous_close": "",
        }
        self.in_th = False
        self.in_td = False
        self.current_th = ""
        self.current_td = ""
        self.capture_mode: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "th":
            self.in_th = True
            self.current_th = ""
        elif tag == "td":
            self.in_td = True
            self.current_td = ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "th":
            self.in_th = False
            text = clean_text(self.current_th)
            if "時価総額" in text:
                self.capture_mode = "market_cap"
            elif "PER" in text:
                self.capture_mode = "per"
            elif "PBR" in text:
                self.capture_mode = "pbr"
            elif "配当利回り" in text:
                self.capture_mode = "dividend_yield"
            elif "信用買残" in text:
                self.capture_mode = "credit_buy"
            elif "信用売残" in text:
                self.capture_mode = "credit_sell"
            elif "貸借倍率" in text:
                self.capture_mode = "credit_ratio"
            elif "前日終値" in text:
                self.capture_mode = "previous_close"
            else:
                self.capture_mode = None
        if tag == "td":
            self.in_td = False
            if self.capture_mode:
                self.metrics[self.capture_mode] = clean_text(self.current_td)
                self.capture_mode = None

    def handle_data(self, data: str) -> None:
        if self.in_th:
            self.current_th += data
        if self.in_td and self.capture_mode:
            self.current_td += data


def extract_stock_name_from_quote_html(page_html: str, symbol: str) -> dict[str, str]:
    parser = TitleParser()
    parser.feed(page_html)
    title = clean_text(parser.title)
    name = ""
    match = re.search(r"(.+?)【" + re.escape(symbol) + r"】", title)
    if match:
        name = match.group(1).strip()
    elif "：" in title:
        name = title.split("：", 1)[0].strip()
    return {"name": name, "page_title": title, "description": clean_text(parser.meta_description)}


def parse_number(value: str) -> float | int | None:
    clean = str(value or "").replace(",", "").replace("%", "").strip()
    if not clean or clean in ["-", "---"]:
        return None
    try:
        num = float(clean)
        return int(num) if num.is_integer() else num
    except ValueError:
        return None


def first_regex(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.DOTALL)
    return clean_text(match.group(1)) if match else ""


def extract_yahoo_quote_from_page(page_html: str) -> dict[str, Any]:
    quote: dict[str, Any] = {"source": "Yahoo Finance JP page"}
    start = page_html.find("_BasePriceBoard__priceInformation")
    end = page_html.find('id="stk_info"', start)
    if start >= 0 and end > start:
        price_region = page_html[start:end]
        values = [
            clean_text(v)
            for v in re.findall(r'_StyledNumber__value[^>]*>(.*?)</span>', price_region, re.DOTALL)
        ]
        if len(values) >= 1:
            quote["price"] = parse_number(values[0])
        if len(values) >= 2:
            quote["change"] = parse_number(values[1])
        if len(values) >= 3:
            quote["change_pct"] = parse_number(values[2])
        quote["quote_time"] = first_regex(r"<time>(.*?)</time>", price_region)

    quote["exchange"] = first_regex(r'_PriceBoardMenu__toggle[^>]*>(.*?)<span', page_html)
    quote["industry"] = first_regex(r'_CommonPriceBoard__industryName[^>]*>(.*?)</a>', page_html)

    def extract_data_item(label: str) -> str:
        label_pos = page_html.find(f">{label}</span>")
        if label_pos < 0:
            return ""
        item_start = page_html.rfind("<dl", 0, label_pos)
        item_end = page_html.find("</dl>", label_pos)
        if item_start < 0 or item_end < 0:
            return ""
        item_html = page_html[item_start:item_end]
        plain = clean_text(item_html)
        if label not in plain:
            return ""
        after_label = plain.split(label, 1)[-1]
        match = re.search(r"[-+]?\d[\d,]*(?:\.\d+)?", after_label)
        if not match:
            return ""
        suffix = ""
        suffix_match = re.search(r"(株|百万円|円|倍|%)", after_label[match.end() : match.end() + 12])
        if suffix_match:
            suffix = suffix_match.group(1)
        return f"{match.group(0)}{suffix}"

    volume_text = extract_data_item("出来高")
    if volume_text:
        quote["volume"] = parse_number(volume_text.replace("株", ""))
    trading_value = extract_data_item("売買代金")
    if trading_value:
        quote["trading_value"] = trading_value
    open_price = extract_data_item("始値")
    high_price = extract_data_item("高値")
    low_price = extract_data_item("安値")
    if open_price:
        quote["open"] = parse_number(open_price)
    if high_price:
        quote["high"] = parse_number(high_price)
    if low_price:
        quote["low"] = parse_number(low_price)
    if quote.get("previous_close") in [None, ""] and isinstance(quote.get("price"), (int, float)) and isinstance(quote.get("change"), (int, float)):
        quote["previous_close"] = quote["price"] - quote["change"]

    return {k: v for k, v in quote.items() if v not in [None, ""]}


def fetch_yahoo_quote_page(symbol: str) -> tuple[dict[str, str], str]:
    url = yahoo_quote_url(symbol)
    page_html = fetch_url(url, referer="https://finance.yahoo.co.jp/", pause=False)
    return extract_stock_name_from_quote_html(page_html, symbol), page_html


def fetch_traders_metrics(code: str, market_hint: str = "") -> dict[str, Any]:
    prefix = get_traders_prefix(market_hint)
    url = f"https://www.traders.co.jp/stocks/{prefix}_{code}/"
    try:
        page_html = fetch_url(url)
        parser = TradersQuoteParser()
        parser.feed(page_html)
        metrics = {k: v for k, v in parser.metrics.items() if v}
        metrics["source"] = "TradersWeb"
        metrics["url"] = url
        return metrics
    except Exception as exc:
        return {"error": str(exc), "source": "TradersWeb", "url": url}


def score_comment(comment: dict[str, Any]) -> tuple[int, dt.datetime, int]:
    text = str(comment.get("text") or "")
    likes = int(comment.get("likes") or 0)
    parsed = parse_jst_datetime(comment.get("date", "")) or dt.datetime(1970, 1, 1)
    age_hours = (now_jst() - parsed).total_seconds() / 3600
    recency = 5 if age_hours <= 6 else 4 if age_hours <= 24 else 2 if age_hours <= 72 else 1
    length = 3 if 30 <= len(text) <= 300 else 2 if len(text) > 300 else 1
    like_score = 4 if likes >= 100 else 3 if likes >= 50 else 2 if likes >= 20 else 1 if likes >= 5 else 0
    keyword_score = min(6, sum(1 for word in INFO_KEYWORDS if word.lower() in text.lower()))
    return recency + length + like_score + keyword_score, parsed, likes


def fetch_yahoo_bbs(symbol: str, hours: int, limit: int) -> dict[str, Any]:
    url = yahoo_forum_url(symbol)
    try:
        page_html = fetch_url(url)
        parser = YahooBBSParser()
        parser.feed(page_html)
        comments = [c for c in parser.comments if within_hours(c.get("date", ""), hours)]
        comments.sort(key=score_comment, reverse=True)
        return {"url": url, "comments": comments[:limit], "count": len(comments), "source": "Yahoo掲示板"}
    except Exception as exc:
        return {"url": url, "comments": [], "count": 0, "source": "Yahoo掲示板", "error": str(exc)}


def calculate_bbs_heat(comments: list[dict[str, Any]]) -> dict[str, Any]:
    parsed_comments = []
    for comment in comments:
        parsed = parse_jst_datetime(comment.get("date", ""))
        if not parsed:
            continue
        age_hours = (now_jst() - parsed).total_seconds() / 3600
        if -0.1 <= age_hours <= 72:
            parsed_comments.append({"age_hours": max(0, age_hours), "likes": int(comment.get("likes") or 0)})

    n_1h = sum(1 for c in parsed_comments if c["age_hours"] <= 1)
    n_3h = sum(1 for c in parsed_comments if c["age_hours"] <= 3)
    n_24h = sum(1 for c in parsed_comments if c["age_hours"] <= 24)
    likes_24h = sum(c["likes"] for c in parsed_comments if c["age_hours"] <= 24)
    top_likes_24h = max([c["likes"] for c in parsed_comments if c["age_hours"] <= 24] or [0])

    if n_1h >= 55:
        level = 8
    elif n_1h >= 35:
        level = 7
    elif n_1h >= 20:
        level = 6
    elif n_1h >= 10:
        level = 5
    elif n_1h >= 5:
        level = 4
    elif n_1h >= 1:
        level = 3
    elif n_24h >= 10 or top_likes_24h >= 30:
        level = 3
    elif n_24h >= 3:
        level = 2
    else:
        level = 1

    if top_likes_24h >= 50 or likes_24h >= 150:
        level = min(10, level + 1)
    label = "低調" if level <= 2 else "やや注目" if level <= 4 else "活況" if level <= 6 else "高熱" if level <= 8 else "過熱"
    return {
        "level": level,
        "label": label,
        "n_1h": n_1h,
        "n_3h": n_3h,
        "n_24h": n_24h,
        "likes_sum_24h": likes_24h,
        "top_likes_24h": top_likes_24h,
    }


def dedupe_news(items: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    output = []
    seen: set[str] = set()
    for item in items:
        title = clean_text(item.get("title", ""))
        link = item.get("link", "")
        if len(title) < 6:
            continue
        signature = re.sub(r"\s+", "", title.lower())[:80]
        if signature in seen:
            continue
        seen.add(signature)
        clean = dict(item)
        clean["title"] = title
        clean["link"] = link
        output.append(clean)
        if len(output) >= limit:
            break
    return output


def fetch_yahoo_news(symbol: str, limit: int) -> dict[str, Any]:
    url = yahoo_news_url(symbol)
    try:
        page_html = fetch_url(url)
        parser = AnchorParser(url)
        parser.feed(page_html)
        items = []
        for anchor in parser.anchors:
            link = anchor["link"]
            title = clean_text(anchor["title"])
            if "finance.yahoo.co.jp" not in link:
                continue
            if "/news/" not in link and "/news" not in link:
                continue
            if title in ["ニュース", "もっと見る", "一覧", "Yahoo!ファイナンス"]:
                continue
            items.append({"title": title, "link": link, "pubDate": "", "source": "Yahooニュース"})
        return {"url": url, "news": dedupe_news(items, limit), "source": "Yahooニュース"}
    except Exception as exc:
        return {"url": url, "news": [], "source": "Yahooニュース", "error": str(exc)}


def fetch_kabutan_news(code: str, limit: int) -> dict[str, Any]:
    url = f"https://kabutan.jp/stock/news?code={urllib.parse.quote(code)}"
    try:
        page_html = fetch_url(url)
        parser = KabutanNewsParser()
        parser.feed(page_html)
        return {
            "url": url,
            "news": dedupe_news(parser.news, limit),
            "company_name": clean_text(parser.company_name),
            "source": "Kabutan",
        }
    except Exception as exc:
        return {"url": url, "news": [], "source": "Kabutan", "error": str(exc)}


def fetch_traders_news(code: str, limit: int, market_hint: str = "") -> dict[str, Any]:
    prefix = get_traders_prefix(market_hint)
    url = f"https://www.traders.co.jp/stocks/{prefix}_{urllib.parse.quote(code)}/news"
    try:
        page_html = fetch_url(url)
        parser = TradersNewsParser()
        parser.feed(page_html)
        return {"url": url, "news": dedupe_news(parser.news, limit), "source": "TradersWeb"}
    except Exception as exc:
        return {"url": url, "news": [], "source": "TradersWeb", "error": str(exc)}


def collect_sources(args: argparse.Namespace) -> dict[str, Any]:
    code, symbol = normalize_symbol(args.stock)
    errors: list[str] = []
    profile: dict[str, Any] = {"code": code, "symbol": symbol}
    quote_page_html = ""
    quote_page_quote: dict[str, Any] = {}

    try:
        quote_page_info, quote_page_html = fetch_yahoo_quote_page(symbol)
        profile.update(quote_page_info)
        quote_page_quote = extract_yahoo_quote_from_page(quote_page_html)
    except Exception as exc:
        errors.append(f"Yahoo quote page: {exc}")

    quote = quote_page_quote
    market_hint = args.market_hint or str(quote.get("exchange") or "")
    metrics = fetch_traders_metrics(code, market_hint)
    if not profile.get("name") and args.name:
        profile["name"] = args.name
    if not profile.get("name") and metrics.get("company_name"):
        profile["name"] = metrics.get("company_name")

    bbs = fetch_yahoo_bbs(symbol, args.hours, args.comments)
    bbs["heat"] = calculate_bbs_heat(bbs.get("comments", []))

    news_groups = []
    if "yahoo" in args.sources:
        news_groups.append(fetch_yahoo_news(symbol, args.news_limit))
    if "kabutan" in args.sources and re.match(r"^\d{3}[0-9A-Z]$", code):
        kabutan = fetch_kabutan_news(code, args.news_limit)
        if not profile.get("name") and kabutan.get("company_name"):
            profile["name"] = kabutan.get("company_name")
        news_groups.append(kabutan)
    if "traders" in args.sources and re.match(r"^\d{3}[0-9A-Z]$", code):
        news_groups.append(fetch_traders_news(code, args.news_limit, market_hint))

    all_news = []
    for group in news_groups:
        for item in group.get("news", []):
            if within_hours(item.get("pubDate", ""), args.hours):
                all_news.append(item)

    def news_sort_key(item: dict[str, str]) -> dt.datetime:
        return parse_jst_datetime(item.get("pubDate", "")) or dt.datetime(1970, 1, 1)

    dated = [n for n in all_news if parse_jst_datetime(n.get("pubDate", ""))]
    undated = [n for n in all_news if not parse_jst_datetime(n.get("pubDate", ""))]
    all_news = sorted(dated, key=news_sort_key, reverse=True) + undated
    all_news = dedupe_news(all_news, args.news_limit)

    return {
        "generated_at_jst": now_jst().strftime("%Y-%m-%d %H:%M:%S"),
        "window_hours": args.hours,
        "profile": profile,
        "quote": quote,
        "metrics": metrics,
        "bbs": bbs,
        "news_groups": news_groups,
        "news": all_news,
        "errors": errors,
    }


def fmt_num(value: Any, digits: int = 2) -> str:
    if isinstance(value, (int, float)):
        if digits == 0:
            return f"{value:,.0f}"
        return f"{value:,.{digits}f}".rstrip("0").rstrip(".")
    if value is None or value == "":
        return "-"
    return str(value)


def render_markdown(data: dict[str, Any], prompt_only: bool = False) -> str:
    profile = data.get("profile", {})
    quote = data.get("quote", {})
    metrics = data.get("metrics", {})
    bbs = data.get("bbs", {})
    heat = bbs.get("heat", {})
    name = profile.get("name") or "-"
    title = f"{profile.get('code')} {name} ({profile.get('symbol')})"

    lines = []
    if not prompt_only:
        lines.append(f"# Codex分析材料: {title}")
        lines.append("")
        lines.append(f"- 生成時刻(JST): {data.get('generated_at_jst')}")
        lines.append(f"- 対象期間: 直近{data.get('window_hours')}時間中心")
        lines.append(f"- Yahoo: {yahoo_quote_url(profile.get('symbol', ''))}")
        lines.append(f"- Yahoo掲示板: {bbs.get('url', '')}")
        lines.append("")
        lines.append("## 基本情報・現在値")
        lines.append(f"- 現値: {fmt_num(quote.get('price'))} {quote.get('currency') or ''}".rstrip())
        lines.append(f"- 前日終値: {fmt_num(quote.get('previous_close'))}")
        lines.append(f"- 騰落: {fmt_num(quote.get('change'))} / {fmt_num(quote.get('change_pct'))}%")
        lines.append(f"- 出来高: {fmt_num(quote.get('volume'), 0)}")
        lines.append(f"- 取引所: {quote.get('exchange') or '-'}")
        lines.append(f"- 時価総額: {metrics.get('market_cap') or '-'}")
        lines.append(f"- PER / PBR: {metrics.get('per') or '-'} / {metrics.get('pbr') or '-'}")
        lines.append(f"- 配当利回り: {metrics.get('dividend_yield') or '-'}")
        lines.append(f"- 信用倍率: {metrics.get('credit_ratio') or '-'}")
        lines.append("")
        lines.append("## ニュース")
        news = data.get("news", [])
        if news:
            for idx, item in enumerate(news, 1):
                date = item.get("pubDate") or "日付不明"
                age = age_label(item.get("pubDate", ""))
                age_suffix = f" / {age}" if age else ""
                lines.append(f"{idx}. [{item.get('source')}] {date}{age_suffix} - {item.get('title')}")
                if item.get("link"):
                    lines.append(f"   {item.get('link')}")
        else:
            lines.append("- 取得できたニュースなし")
        lines.append("")
        lines.append("## Yahoo掲示板")
        lines.append(
            f"- 人気度: {heat.get('level', '-')}/10 {heat.get('label', '')} "
            f"(1h:{heat.get('n_1h', 0)}, 3h:{heat.get('n_3h', 0)}, 24h:{heat.get('n_24h', 0)}, "
            f"24h likes:{heat.get('likes_sum_24h', 0)}, top:{heat.get('top_likes_24h', 0)})"
        )
        comments = bbs.get("comments", [])
        if comments:
            for idx, item in enumerate(comments, 1):
                age = age_label(item.get("date", ""))
                age_suffix = f" / {age}" if age else ""
                text = clean_text(item.get("text", ""))
                lines.append(f"{idx}. {item.get('date') or '日付不明'}{age_suffix} / 👍{item.get('likes', 0)}")
                lines.append(f"   {text}")
        else:
            lines.append("- 取得できた投稿なし")
        errors = data.get("errors") or []
        for group in data.get("news_groups", []):
            if group.get("error"):
                errors.append(f"{group.get('source')}: {group.get('error')}")
        if bbs.get("error"):
            errors.append(f"Yahoo掲示板: {bbs.get('error')}")
        if metrics.get("error"):
            errors.append(f"Traders metrics: {metrics.get('error')}")
        if errors:
            lines.append("")
            lines.append("## 取得エラー")
            for err in errors:
                lines.append(f"- {err}")
        lines.append("")

    lines.append("## Codexへの分析指示")
    lines.append(
        "上の材料だけを根拠に、この株の直近異動理由を中国語で分析してください。"
        "ニュースを最優先、Yahoo掲示板は市場心理・未確認材料として補助扱いにしてください。"
        "回答は最低3〜4行、材料が十分なら短い市場ニュース記事くらいの詳しさにしてください。"
        "出力は 1) 最有力理由 2) 補助理由 3) 掲示板温度 4) 確度 5) 注意点 の順。"
        "材料が弱い場合は断定せず、「思惑」「期待」「確認待ち」と明記してください。"
    )
    return "\n".join(lines).strip() + "\n"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect Yahoo forum, stock news, quote, and metrics for Codex stock-move analysis."
    )
    parser.add_argument("stock", help="Japanese stock code or Yahoo symbol, e.g. 7203, 285A, 7203.T")
    parser.add_argument("--name", default="", help="Optional stock name override")
    parser.add_argument("--market-hint", default="", help="Optional market hint for Traders prefix, e.g. 東証G")
    parser.add_argument("--hours", type=int, default=24, help="Recent evidence window in hours")
    parser.add_argument("--comments", type=int, default=20, help="Max Yahoo forum comments to print")
    parser.add_argument("--news-limit", type=int, default=12, help="Max news items to print")
    parser.add_argument(
        "--sources",
        default="yahoo,kabutan,traders",
        help="Comma-separated news sources: yahoo,kabutan,traders",
    )
    parser.add_argument("--format", choices=["markdown", "json", "prompt"], default="markdown")
    parser.add_argument("--output", default="", help="Write output to this path instead of stdout")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    args.sources = {s.strip().lower() for s in args.sources.split(",") if s.strip()}
    try:
        data = collect_sources(args)
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        output = json.dumps(data, ensure_ascii=False, indent=2)
    elif args.format == "prompt":
        output = render_markdown(data, prompt_only=True)
    else:
        output = render_markdown(data)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
