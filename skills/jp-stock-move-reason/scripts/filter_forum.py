#!/usr/bin/env python3
"""Filter supplied Yahoo forum comments offline using the collector's algorithm."""
import argparse
import datetime as dt
import json
from pathlib import Path

from stock_move_sources import JST, select_yahoo_comments


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON object with comments and timezone-aware as_of")
    args = parser.parse_args()
    packet = json.loads(args.input.read_text(encoding="utf-8"))
    current = dt.datetime.fromisoformat(packet["as_of"])
    if current.tzinfo is None:
        parser.error("as_of must include a timezone offset")
    comments = packet["comments"]
    if not isinstance(comments, list) or any(not isinstance(c, dict) for c in comments):
        parser.error("comments must be a list of objects")
    result = select_yahoo_comments(comments, current=current.astimezone(JST).replace(tzinfo=None))
    result.pop("cached_comments")
    result.update(as_of=packet["as_of"], input_mode="supplied_comments", network_used=False)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
