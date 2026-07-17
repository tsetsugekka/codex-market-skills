#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rank Kabutan PTS movers by computed turnover.

This helper is intentionally small and public-safe. It fetches Kabutan PTS day
or night mover pages, filters movers by percentage change, and ranks by:

    PTS price * PTS volume

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
class PtsRow:
    code: str
    name: str
    market: str
    close: float
    pts_price: float
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
    """Select Kabutan PTS section by JST clock.

    Trading-day 08:20-16:30 uses day section, including the 15:30-16:30
    after-close window. Night section is used for weekends and all other times.
    Japanese exchange holidays are not embedded; pass --session night if the
    date is a known non-trading weekday.
    """
    if as_of.weekday() >= 5:
        return "night"
    current = as_of.time()
    if dt.time(8, 20) <= current < dt.time(16, 30):
        return "day"
    return "night"


def extract_stamp(html_text: str) -> str:
    text = clean_text(re.sub(r"<[^>]+>", "\n", html_text))
    match = re.search(r"(\d{4}年\d{2}月\d{2}日)\s+(\d{1,2}:\d{2}現在)", text)
    return f"{match.group(1)} {match.group(2)}" if match else ""


def parse_rows(html_text: str, page: int) -> list[PtsRow]:
    parser = StockTableParser()
    parser.feed(html_text)
    rows: list[PtsRow] = []
    for cells in parser.rows:
        if len(cells) < 10:
            continue
        close = parse_number(cells[5])
        pts_price = parse_number(cells[6])
        diff = parse_number(cells[7])
        pct = parse_number(cells[8])
        volume = parse_number(cells[9])
        if close is None or pts_price is None or diff is None or pct is None or volume is None:
            continue
        rows.append(
            PtsRow(
                code=cells[0],
                name=cells[1],
                market=cells[2],
                close=close,
                pts_price=pts_price,
                diff=diff,
                pct=pct,
                volume=int(volume),
                turnover=pts_price * volume,
                page=page,
            )
        )
    return rows


def is_etf(row: PtsRow) -> bool:
    return "東Ｅ" in row.market or row.name.startswith(("日経", "ＴＰＸ", "上場", "ｉＦ", "ＭＸ", "ＧＸ", "楽天", "ＮＦ", "ｉＳ"))


def collect_side(session: str, side: str, min_abs_pct: float, max_pages: int) -> tuple[str, list[PtsRow]]:
    all_rows: list[PtsRow] = []
    stamp = ""
    for page in range(1, max_pages + 1):
        html_text = fetch_url(build_url(session, side, page), pause=page > 1)
        stamp = extract_stamp(html_text) or stamp
        rows = parse_rows(html_text, page)
        if not rows:
            break
        all_rows.extend(rows)
        last_pct = rows[-1].pct
        if side == "increase" and last_pct < min_abs_pct:
            break
        if side == "decrease" and last_pct > -min_abs_pct:
            break
    return stamp, all_rows


def filter_rows(rows: Iterable[PtsRow], side: str, min_abs_pct: float, exclude_etf: bool) -> list[PtsRow]:
    result: list[PtsRow] = []
    for row in rows:
        if exclude_etf and is_etf(row):
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


def print_markdown(side: str, rows: list[PtsRow], top: int, stamp: str, session: str) -> None:
    title = "涨幅" if side == "increase" else "跌幅"
    section_name = "日中" if session == "day" else "夜间"
    print(f"## PTS{section_name}{title}榜 成交额Top{top}")
    if stamp:
        print(f"- Kabutan时间: {stamp}")
    print(f"- Kabutan section: pts_{session}_price_{side}")
    print("- 口径: 先按 PTS涨跌幅过滤，再按 `PTS株价 × PTS出来高` 排序")
    print()
    print("| 排名 | 代码 | 名称 | 市场 | PTS价 | 涨跌幅 | 出来高 | 估算成交额 |")
    print("|---:|---|---|---|---:|---:|---:|---:|")
    for index, row in enumerate(rows[:top], 1):
        print(
            f"| {index} | {row.code} | {row.name} | {row.market} | "
            f"{row.pts_price:g} | {row.pct:+.2f}% | {row.volume:,} | {format_amount(row.turnover)} |"
        )
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank Kabutan PTS movers by computed turnover.")
    parser.add_argument(
        "--session",
        choices=["auto", "night", "day"],
        default="auto",
        help="PTS section to inspect. auto uses JST clock: day on trading weekdays 08:20-16:30, otherwise night.",
    )
    parser.add_argument(
        "--as-of",
        help="JST datetime for --session auto, e.g. 2026-07-17T15:45. Defaults to now.",
    )
    parser.add_argument("--side", choices=["increase", "decrease", "both"], default="both")
    parser.add_argument("--min-abs-pct", type=float, default=3.0, help="Minimum absolute PTS change percentage.")
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
        ranked = filter_rows(rows, side, args.min_abs_pct, args.exclude_etf)
        top_rows = ranked[: args.top]
        selected_codes.extend(row.code for row in top_rows)
        output["sides"][side] = {"stamp": stamp, "rows": [asdict(row) for row in top_rows]}
        if args.format == "markdown":
            print_markdown(side, ranked, args.top, stamp, session)

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
