# Python collection and offline forum filtering

The release bundles `scripts/stock_move_sources.py`, `scripts/pts_turnover_ranking.py` and `scripts/filter_forum.py` under this Skill. They use Python 3.10+ and the standard library; no API key is included. Paths below are relative to the installed Skill directory. Locate the actual installed directory before executing; a source link is not a promise that a host can run Python.

## Python with network access

For an individual stock:

```sh
python3 scripts/stock_move_sources.py 7203 --format json
```

For an estimated-turnover ranking, first read [ranking rules](pts-turnover-ranking.md), then:

```sh
python3 scripts/pts_turnover_ranking.py --session auto --side both --top 10 --format json
python3 scripts/stock_move_sources.py 7203 --forum-only --comments 100 --format json
```

Replace the example code with each selected code; collect sequentially and only once per stock per turn. The collector defaults to 12 news items and at most 100 forum posts; `--forum-only` skips other sources. `--comments 0` disables forum fetching. Output goes to stdout unless `--output` is explicitly supplied. Yahoo throttling uses a temporary shared state/lock and enforces its cooldown; do not clear it to force another request. No account access or trading occurs.

## Python without network access

Use comments already supplied by the user or read through an available authorized browser/connector. Save the one-stock collection as UTF-8 JSON:

```json
{
  "as_of": "2026-09-21T12:00:00+09:00",
  "comments": [
    {"date": "2026/09/21 11:30", "likes": 12, "text": "業績予想の上方修正と増配に関する発表を確認したい"}
  ]
}
```

`as_of` is the actual collection/analysis reference time with an offset, not an invented current timestamp. Comment dates are JST `YYYY/MM/DD HH:MM`; yearless `MM/DD HH:MM` is resolved against `as_of`, including the year boundary. Keep each stock separate and record the source and coverage in the report.

```sh
python3 scripts/filter_forum.py comments.json
```

This command reads only that file and writes JSON to stdout; it performs no network requests and creates no cache. It uses the same `select_yahoo_comments` function as live collection: latest 100 raw posts; raw 24h count decides 24h versus 72h; then five-like minimum, quality score, normalized first-60-character deduplication, at most 20 shortlisted, and newest five by time/likes. The output includes counts, selected window and the full text of at most five selected comments. An empty selection means no supplied posts passed, not that the market had no discussion. Missing likes or dates cannot be invented.

## No Python execution

Read available evidence and apply the documented selection rules manually when the supplied sample is small enough to verify. Report the sample size and any incomplete scoring/deduplication. Do not claim the full pipeline ran or invent a numerical heat score. A ranking can still show verified quotes and catalysts with an explicit forum-coverage gap.

Package acceptance, Python execution and network access are separate capabilities. ChatGPT Web, ChatGPT work and Codex must each use the tools actually exposed in that session.
