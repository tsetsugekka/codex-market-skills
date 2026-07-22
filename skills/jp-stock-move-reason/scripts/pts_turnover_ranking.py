#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rank Kabutan Japanese-stock movers by computed turnover.

This helper is intentionally small and public-safe. During regular Tokyo market
hours it reads Kabutan's regular price-mover pages. Around the open, lunch break,
after the close, and overnight it reads the appropriate PTS section. It filters
movers by percentage change and volume, then ranks by:

    current price * volume

It does not infer reasons. Use stock_move_sources.py for the resulting stock
codes when reasons are needed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import html
import json
import random
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from typing import Iterable


JST = dt.timezone(dt.timedelta(hours=9), "JST")
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


@dataclass
class MoverRow:
    code: str
    name: str
    market: str
    reference_price: float
    price: float
    diff: float
    pct: float
    volume: int
    turnover: float
    page: int


class StockTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_table = False
        self.table_depth = 0
        self.in_tbody = False
        self.in_row = False
        self.in_cell = False
        self.current_cell: list[str] = []
        self.current_row: list[str] = []
        self.rows: list[list[str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = {k: v or "" for k, v in attrs}
        if tag == "table" and "stock_table" in attrs_d.get("class", ""):
            self.in_table = True
            self.table_depth = 1
            return
        if self.in_table and tag == "table":
            self.table_depth += 1
        if self.in_table and tag == "tbody":
            self.in_tbody = True
        if self.in_tbody and tag == "tr":
            self.in_row = True
            self.current_row = []
        if self.in_row and tag in {"td", "th"}:
            self.in_cell = True
            self.current_cell = []

    def handle_endtag(self, tag: str) -> None:
        if self.in_cell and tag in {"td", "th"}:
            self.in_cell = False
            self.current_row.append(clean_text("".join(self.current_cell)))
        elif self.in_row and tag == "tr":
            self.in_row = False
            if self.current_row:
                self.rows.append(self.current_row)
        elif self.in_table and tag == "tbody":
            self.in_tbody = False
        elif self.in_table and tag == "table":
            self.table_depth -= 1
            if self.table_depth <= 0:
                self.in_table = False

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.current_cell.append(data)


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    return re.sub(r"\s+", " ", value).strip()


def parse_number(value: str) -> float | None:
    value = clean_text(value).replace(",", "").replace("%", "")
    if value in {"", "-", "－", "--"}:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def fetch_url(url: str, pause: bool = True) -> str:
    if pause:
        time.sleep(random.uniform(0.8, 1.8))
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "https://kabutan.jp/",
            "Cookie": "shared_perpage=50",
            "Cache-Control": "max-age=0",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        body = response.read()
        encoding = response.info().get("Content-Encoding", "")
        if encoding == "gzip":
            body = gzip.decompress(body)
        elif encoding == "deflate":
            import zlib

            body = zlib.decompress(body)
        return body.decode("utf-8", errors="ignore")


def build_url(session: str, side: str, page: int) -> str:
    params = {
        "market": "0",
        "capitalization": "-1",
        "dispmode": "normal",
        "page": str(page),
        "cachebust": dt.datetime.now(JST).strftime("%Y%m%d%H%M%S"),
    }
    if session == "regular":
        params["mode"] = "2_1" if side == "increase" else "2_2"
        return "https://kabutan.jp/warning/?" + urllib.parse.urlencode(params)
    return f"https://kabutan.jp/warning/pts_{session}_price_{side}?" + urllib.parse.urlencode(params)


def parse_as_of(value: str | None) -> dt.datetime:
    if not value:
        return dt.datetime.now(JST)
    normalized = value.strip()
    if normalized.endswith("Z"):
        parsed = dt.datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    else:
        parsed = dt.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=JST)
    return parsed.astimezone(JST)


def auto_session(as_of: dt.datetime) -> str:
    """Select the Kabutan regular/PTS section by JST clock.

    On trading weekdays, regular market pages are used during the morning and
    afternoon cash sessions. PTS day pages cover pre-open, lunch, and after-close
    windows. PTS night is used at all other times and on weekends. Japanese
    exchange holidays are not embedded; pass --session night on known holidays.
    """
    if as_of.weekday() >= 5:
        return "night"
    current = as_of.time()
    if dt.time(9, 0) <= current < dt.time(11, 30):
        return "regular"
    if dt.time(12, 30) <= current < dt.time(15, 30):
        return "regular"
    if dt.time(8, 0) <= current < dt.time(9, 0):
        return "day"
    if dt.time(11, 30) <= current < dt.time(12, 30):
        return "day"
    if dt.time(15, 30) <= current < dt.time(17, 0):
        return "day"
    return "night"


def extract_stamp(html_text: str) -> str:
    text = clean_text(re.sub(r"<[^>]+>", "\n", html_text))
    match = re.search(r"(\d{4}年\d{2}月\d{2}日)\s+(\d{1,2}:\d{2}現在)", text)
    return f"{match.group(1)} {match.group(2)}" if match else ""


def parse_rows(html_text: str, page: int, session: str) -> list[MoverRow]:
    parser = StockTableParser()
    parser.feed(html_text)
    rows: list[MoverRow] = []
    for cells in parser.rows:
        if len(cells) < 10:
            continue
        if session == "regular":
            price = parse_number(cells[5])
            diff = parse_number(cells[7])
            pct = parse_number(cells[8])
            volume = parse_number(cells[9])
            reference_price = price - diff if price is not None and diff is not None else None
        else:
            reference_price = parse_number(cells[5])
            price = parse_number(cells[6])
            diff = parse_number(cells[7])
            pct = parse_number(cells[8])
            volume = parse_number(cells[9])
        if reference_price is None or price is None or diff is None or pct is None or volume is None:
            continue
        rows.append(
            MoverRow(
                code=cells[0],
                name=cells[1],
                market=cells[2],
                reference_price=reference_price,
                price=price,
                diff=diff,
                pct=pct,
                volume=int(volume),
                turnover=price * volume,
                page=page,
            )
        )
    return rows


def is_etf(row: MoverRow) -> bool:
    return "東Ｅ" in row.market or row.name.startswith(("日経", "ＴＰＸ", "上場", "ｉＦ", "ＭＸ", "ＧＸ", "楽天", "ＮＦ", "ｉＳ"))


def collect_side(session: str, side: str, min_abs_pct: float, max_pages: int) -> tuple[str, list[MoverRow]]:
    all_rows: list[MoverRow] = []
    stamp = ""
    for page in range(1, max_pages + 1):
        html_text = fetch_url(build_url(session, side, page), pause=page > 1)
        stamp = extract_stamp(html_text) or stamp
        rows = parse_rows(html_text, page, session)
        if not rows:
            break
        all_rows.extend(rows)
        last_pct = rows[-1].pct
        if side == "increase" and last_pct < min_abs_pct:
            break
        if side == "decrease" and last_pct > -min_abs_pct:
            break
    return stamp, all_rows


def filter_rows(
    rows: Iterable[MoverRow],
    side: str,
    min_abs_pct: float,
    min_volume: int,
    exclude_etf: bool,
) -> list[MoverRow]:
    result: list[MoverRow] = []
    for row in rows:
        if exclude_etf and is_etf(row):
            continue
        if row.volume <= min_volume:
            continue
        if side == "increase" and row.pct >= min_abs_pct:
            result.append(row)
        elif side == "decrease" and row.pct <= -min_abs_pct:
            result.append(row)
    return sorted(result, key=lambda row: row.turnover, reverse=True)


def format_amount(value: float) -> str:
    if abs(value) >= 100_000_000:
        return f"{value / 100_000_000:.2f}亿日元"
    if abs(value) >= 10_000:
        return f"{value / 10_000:.1f}万日元"
    return f"{value:.0f}日元"


def print_markdown(
    side: str,
    rows: list[MoverRow],
    top: int,
    stamp: str,
    session: str,
    min_abs_pct: float,
    min_volume: int,
) -> None:
    prefix = "" if session == "regular" else "PTS"
    title = (
        f"{prefix}上涨 Top10（涨幅大于3%/成交量大于2000/成交额排序）"
        if side == "increase"
        else f"{prefix}下跌 Top10（跌幅大于3%/成交量大于2000/成交额排序）"
    )
    section_name = {"regular": "东京市场日中", "day": "PTS日中", "night": "PTS夜间"}[session]
    section_url = (
        f"warning/?mode={'2_1' if side == 'increase' else '2_2'}"
        if session == "regular"
        else f"pts_{session}_price_{side}"
    )
    price_label = "现价" if session == "regular" else "PTS价"
    pct_label = "涨跌幅" if session == "regular" else "PTS涨跌幅"
    volume_label = "出来高" if session == "regular" else "PTS出来高"
    print(f"## {title}")
    if stamp:
        print(f"- Kabutan时间: {stamp}")
    print(f"- 数据时段: {section_name}")
    print(f"- Kabutan section: {section_url}")
    print(
        f"- 口径: 先筛 `abs({pct_label}) >= {min_abs_pct:g}%` 且 "
        f"`{volume_label} > {min_volume:,}`，再按 `{price_label} × {volume_label}` 排序"
    )
    print()
    print(f"| 排名 | 代码 | 名称 | 市场 | {price_label} | 涨跌幅 | 出来高 | 估算成交额 |")
    print("|---:|---|---|---|---:|---:|---:|---:|")
    for index, row in enumerate(rows[:top], 1):
        print(
            f"| {index} | {row.code} | {row.name} | {row.market} | "
            f"{row.price:g} | {row.pct:+.2f}% | {row.volume:,} | {format_amount(row.turnover)} |"
        )
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank Kabutan regular/PTS movers by computed turnover.")
    parser.add_argument(
        "--session",
        choices=["auto", "regular", "night", "day"],
        default="auto",
        help=(
            "Section to inspect. auto uses regular pages during 09:00-11:30 and 12:30-15:30 JST; "
            "PTS day during 08:00-09:00, 11:30-12:30, and 15:30-17:00; otherwise PTS night."
        ),
    )
    parser.add_argument(
        "--as-of",
        help="JST datetime for --session auto, e.g. 2026-07-17T15:45. Defaults to now.",
    )
    parser.add_argument("--side", choices=["increase", "decrease", "both"], default="both")
    parser.add_argument("--min-abs-pct", type=float, default=3.0, help="Minimum absolute change percentage.")
    parser.add_argument(
        "--min-volume",
        type=int,
        default=2000,
        help="Minimum exclusive volume threshold. Default keeps rows with volume > 2000.",
    )
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--max-pages", type=int, default=20)
    parser.add_argument("--exclude-etf", action="store_true", help="Exclude ETF/ETN-like rows.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument(
        "--reason-commands",
        action="store_true",
        help="Also print stock_move_sources.py commands for the selected codes.",
    )
    args = parser.parse_args()

    as_of = parse_as_of(args.as_of)
    session = auto_session(as_of) if args.session == "auto" else args.session
    sides = ["increase", "decrease"] if args.side == "both" else [args.side]
    output: dict[str, object] = {"session": session, "as_of_jst": as_of.isoformat(), "sides": {}}
    selected_codes: list[str] = []

    for side in sides:
        stamp, rows = collect_side(session, side, args.min_abs_pct, args.max_pages)
        ranked = filter_rows(rows, side, args.min_abs_pct, args.min_volume, args.exclude_etf)
        top_rows = ranked[: args.top]
        selected_codes.extend(row.code for row in top_rows)
        output["sides"][side] = {
            "stamp": stamp,
            "min_abs_pct": args.min_abs_pct,
            "min_volume_exclusive": args.min_volume,
            "rows": [asdict(row) for row in top_rows],
        }
        if args.format == "markdown":
            print_markdown(side, ranked, args.top, stamp, session, args.min_abs_pct, args.min_volume)

    if args.format == "json":
        print(json.dumps(output, ensure_ascii=False, indent=2))
    elif args.reason_commands:
        print("## Reason collection commands")
        for code in dict.fromkeys(selected_codes):
            print(
                "python3 skills/jp-stock-move-reason/scripts/stock_move_sources.py "
                f"{code} --format markdown --hours 48 --comments 12 --news-limit 10"
            )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
