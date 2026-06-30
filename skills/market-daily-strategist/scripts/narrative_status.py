#!/usr/bin/env python3
"""Fetch and filter a 24h market narrative status JSON feed.

This helper is intentionally narrow: it is an optional pre-screen for market
reports, not a primary news or price source.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any


DEFAULT_URL = "https://daytrading.monster/tools/24hfeed/narrative_status.json"

MARKET_KEYS = {
    "us": ["ai", "us_iran", "commodities", "rates_bonds", "spx_gamma", "non_ai", "crypto"],
    "jp": ["nikkei", "ai", "commodities", "rates_bonds", "us_iran", "non_ai"],
    "cn": ["cn_market", "commodities", "rates_bonds", "us_iran", "ai"],
    "global": ["us_iran", "commodities", "rates_bonds", "spx_gamma", "nikkei", "cn_market", "crypto"],
    "crypto": ["crypto", "rates_bonds", "spx_gamma"],
}


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        normalized = value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized).astimezone(timezone.utc)
    except ValueError:
        return None


def age_hours(timestamp: datetime | None, now: datetime) -> float | None:
    if timestamp is None:
        return None
    return (now - timestamp).total_seconds() / 3600


def fetch_json(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "codex-market-skills/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read()
    return json.loads(payload)


def select_keys(market: str) -> list[str]:
    if market == "all":
        return []
    return MARKET_KEYS[market]


def entry_fresh(entry: dict[str, Any], now: datetime, max_entry_age_hours: float) -> tuple[bool, float | None]:
    source_time = parse_time(entry.get("sourceCreatedAt"))
    updated_time = parse_time(entry.get("updatedAt"))
    primary_time = source_time or updated_time
    entry_age = age_hours(primary_time, now)
    if entry_age is None:
        return False, None
    return entry_age <= max_entry_age_hours, entry_age


def build_summary(data: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    generated_at = parse_time(data.get("generatedAt"))
    reviewed_at = parse_time(data.get("reviewedAt"))
    feed_age = age_hours(generated_at or reviewed_at, now)
    feed_is_fresh = feed_age is not None and feed_age <= args.max_feed_age_hours

    wanted_keys = set(select_keys(args.market))
    items = []
    for item in data.get("items", []):
        key = item.get("key")
        if wanted_keys and key not in wanted_keys:
            continue
        fresh_entries = []
        stale_entries = 0
        for entry in item.get("entries", []):
            is_fresh, entry_age = entry_fresh(entry, now, args.max_entry_age_hours)
            if not is_fresh:
                stale_entries += 1
                continue
            fresh_entries.append(
                {
                    "text": entry.get("text"),
                    "direction": entry.get("direction"),
                    "updatedAt": entry.get("updatedAt"),
                    "sourceCreatedAt": entry.get("sourceCreatedAt"),
                    "ageHours": None if entry_age is None else round(entry_age, 2),
                    "evidenceTweetIds": entry.get("evidenceTweetIds", []),
                }
            )
            if len(fresh_entries) >= args.limit:
                break
        items.append(
            {
                "key": key,
                "label": item.get("label"),
                "freshEntries": fresh_entries,
                "staleEntriesSkipped": stale_entries,
                "topDirection": item.get("direction"),
                "topText": item.get("text"),
                "updatedAt": item.get("updatedAt"),
            }
        )

    return {
        "status": "ok" if feed_is_fresh else "stale_feed",
        "generatedAt": data.get("generatedAt"),
        "reviewedAt": data.get("reviewedAt"),
        "feedAgeHours": None if feed_age is None else round(feed_age, 2),
        "maxFeedAgeHours": args.max_feed_age_hours,
        "maxEntryAgeHours": args.max_entry_age_hours,
        "market": args.market,
        "items": items,
        "discipline": "Use as a narrative pre-screen only; verify facts, prices, and market reaction elsewhere.",
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# Narrative Status ({summary['market']})",
        "",
        f"- status: {summary['status']}",
        f"- generatedAt: {summary.get('generatedAt')}",
        f"- reviewedAt: {summary.get('reviewedAt')}",
        f"- feedAgeHours: {summary.get('feedAgeHours')} / max {summary.get('maxFeedAgeHours')}",
        f"- entryFreshnessHours: max {summary.get('maxEntryAgeHours')}",
        "- use: narrative pre-screen only; verify facts, prices, and market reaction elsewhere",
        "",
    ]
    for item in summary["items"]:
        entries = item["freshEntries"]
        if not entries:
            continue
        lines.append(f"## {item['key']} - {item.get('label')}")
        for entry in entries:
            ids = ",".join(entry.get("evidenceTweetIds") or [])
            lines.append(
                f"- {entry.get('direction')}: {entry.get('text')} "
                f"(sourceCreatedAt={entry.get('sourceCreatedAt')}, ageHours={entry.get('ageHours')}, evidenceTweetIds={ids})"
            )
        if item["staleEntriesSkipped"]:
            lines.append(f"- skipped stale entries: {item['staleEntriesSkipped']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--market", choices=["us", "jp", "cn", "global", "crypto", "all"], default="global")
    parser.add_argument("--limit", type=int, default=5, help="Fresh entries per narrative key")
    parser.add_argument("--max-feed-age-hours", type=float, default=6.0)
    parser.add_argument("--max-entry-age-hours", type=float, default=24.0)
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        data = fetch_json(args.url, args.timeout)
        summary = build_summary(data, args)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(summary))
    return 0 if summary["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
