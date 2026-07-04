#!/usr/bin/env python3
"""Fetch Japan earnings schedule rows from SBI Securities.

The SBI page is an ETGate shell that embeds the real Iris calendar API URL and
a volatile hash parameter in inline JavaScript. Do not call the JSONP endpoint
with only selectedDate; it returns "<!-- ERROR Calendar -->".
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import urllib.request
from typing import Any


DEFAULT_ENTRY_URL = (
    "https://www.sbisec.co.jp/ETGate/?_ControlID=WPLETmgR001Control"
    "&_PageID=WPLETmgR001Mdtl20"
    "&_DataStoreID=DSWPLETmgR001Control"
    "&_ActionID=DefaultAID"
    "&burl=iris_economicCalendar"
    "&cat1=market"
    "&cat2=economicCalender"
    "&dir=tl1-cal%7Ctl2-schedule%7Ctl3-stock%7Ctl4-calsel"
    "&file=index.html"
    "&getFlg=on"
)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def fetch_bytes(url: str) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        content_type = resp.headers.get("Content-Type", "")
        return resp.read(), content_type


def decode_sbi(data: bytes, content_type: str = "") -> str:
    match = re.search(r"charset=([A-Za-z0-9_-]+)", content_type, re.I)
    encodings = []
    if match:
        declared = match.group(1)
        if declared.lower() in {"windows-31j", "ms932"}:
            declared = "cp932"
        encodings.append(declared)
    encodings.extend(["shift_jis", "cp932", "utf-8"])
    for encoding in encodings:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("shift_jis", errors="replace")


def extract_js_var(html_text: str, name: str) -> str:
    pattern = rf"var\s+{re.escape(name)}\s*=\s*['\"]([^'\"]+)['\"]"
    match = re.search(pattern, html_text)
    if not match:
        raise RuntimeError(f"Could not find SBI JavaScript variable: {name}")
    return html.unescape(match.group(1))


def discover_sbi_api(entry_url: str) -> dict[str, str]:
    data, content_type = fetch_bytes(entry_url)
    html_text = decode_sbi(data, content_type)
    return {
        "entry_url": entry_url,
        "announce_info_date": extract_js_var(html_text, "ANNOUNCE_INFO_DATE"),
        "announce_info_param": extract_js_var(html_text, "ANNOUNCE_INFO_PARAM"),
        "announce_calendar_url": extract_js_var(html_text, "ANNOUNCE_CALENDAR_URL"),
        "announce_calendar_param": extract_js_var(html_text, "ANNOUNCE_CALENDAR_PARAM"),
    }


def normalize_jsonp_payload(text: str) -> str:
    stripped = text.strip()
    if "ERROR Calendar" in stripped:
        raise RuntimeError("SBI returned ERROR Calendar")
    if stripped.startswith("("):
        stripped = stripped[1:]
    if stripped.endswith(");"):
        stripped = stripped[:-2]
    elif stripped.endswith(")"):
        stripped = stripped[:-1]
    stripped = stripped.strip()
    # SBI keeps the top-level key `link` unquoted while the rest is JSON-like.
    stripped = re.sub(r"(?m)^(\s*)link\s*:", r'\1"link":', stripped)
    return stripped


def parse_sbi_payload(data: bytes, content_type: str) -> dict[str, Any]:
    text = decode_sbi(data, content_type)
    payload = normalize_jsonp_payload(text)
    return json.loads(payload)


def clean_cell(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def fetch_earnings_for_date(api: dict[str, str], yyyymmdd: str) -> list[dict[str, Any]]:
    # The param extracted from JS starts with "?" and already contains SBI's volatile hash.
    url = f"{api['announce_info_date']}{api['announce_info_param']}&selectedDate={yyyymmdd}"
    data, content_type = fetch_bytes(url)
    parsed = parse_sbi_payload(data, content_type)
    rows = []
    for row in parsed.get("body", []):
        rows.append(
            {
                "date": yyyymmdd,
                "product_code": clean_cell(row.get("productCode")),
                "product_name": clean_cell(row.get("productName")),
                "exchange_code": clean_cell(row.get("exchangeCode")),
                "time": clean_cell(row.get("time")),
                "order_time": clean_cell(row.get("orderTime")),
                "type": clean_cell(row.get("type")),
                "estimate": clean_cell(row.get("estimate")),
                "consensus": clean_cell(row.get("consensus")),
                "announcement_kbn": clean_cell(row.get("announcementKbn")),
            }
        )
    return rows


def week_dates(week_start: str) -> list[str]:
    start = dt.date.fromisoformat(week_start)
    return [(start + dt.timedelta(days=i)).strftime("%Y%m%d") for i in range(5)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--date", action="append", help="Date as YYYYMMDD. May be repeated.")
    group.add_argument("--week-start", help="Monday date as YYYY-MM-DD; fetch Mon-Fri.")
    parser.add_argument("--entry-url", default=DEFAULT_ENTRY_URL, help="SBI ETGate entry URL.")
    parser.add_argument("--format", choices=["json", "tsv"], default="json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dates = args.date if args.date else week_dates(args.week_start)
    api = discover_sbi_api(args.entry_url)
    rows: list[dict[str, Any]] = []
    for yyyymmdd in dates:
        rows.extend(fetch_earnings_for_date(api, yyyymmdd))

    if args.format == "json":
        print(json.dumps({"source": api["entry_url"], "rows": rows}, ensure_ascii=False, indent=2))
    else:
        fields = ["date", "order_time", "product_code", "product_name", "exchange_code", "type", "estimate", "consensus"]
        print("\t".join(fields))
        for row in rows:
            print("\t".join(str(row.get(field, "")) for field in fields))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
