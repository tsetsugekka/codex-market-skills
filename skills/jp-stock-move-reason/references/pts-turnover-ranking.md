# PTS Turnover Ranking Sub-skill

Use this sub-skill when the user asks for Kabutan PTS day or night mover lists
ranked by trading value / turnover, especially phrases such as:

- `PTS夜间涨跌榜成交额Top10`
- `PTS日中涨跌幅3%以上成交额`
- `涨跌幅3%以上的成交额top10`
- `不是成交量，是成交额`

## Core Rule

Kabutan PTS warning pages show PTS price and PTS volume, but not always the
turnover column in the list view. Compute turnover as:

```text
computed_turnover = PTS株価 * PTS出来高
```

Default screening is:

```text
abs(PTS騰落率) >= 3%
PTS出来高 > 2000
```

Then rank by `computed_turnover`, not by page order and not by volume alone.

## Sources

Use the rendered/current Kabutan warning pages, with 50 rows per page via the
`shared_perpage=50` cookie:

- Night increase: `https://kabutan.jp/warning/pts_night_price_increase`
- Night decrease: `https://kabutan.jp/warning/pts_night_price_decrease`
- Day increase: `https://kabutan.jp/warning/pts_day_price_increase`
- Day decrease: `https://kabutan.jp/warning/pts_day_price_decrease`

## Section Selection

Default to `--session auto`. The helper selects by JST clock:

- Trading weekdays `08:20-15:30` 日中取引: use day-section URLs.
- Trading weekdays `15:30-16:30` 大引け後: still use day-section URLs.
- `17:00-06:00` 夜間取引: use night-section URLs.
- Outside the day/after-close windows, weekends, and known non-trading days:
  use night-section URLs.

The script handles weekends automatically. If today is a Japanese exchange
holiday on a weekday, pass `--session night` explicitly.

For day-session PTS, remember Kabutan compares:

- `08:20-15:29`: against the previous regular-session close.
- `15:30+`: against the same-day regular-session close.

For night-session PTS, compare against the same-day regular-session close.

## Helper Script

Run from the repository root:

```bash
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py \
  --session auto \
  --side both \
  --min-abs-pct 3 \
  --min-volume 2000 \
  --top 10 \
  --reason-commands
```

Useful variants:

```bash
# Auto-select day/night section from JST clock
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py --side both

# Force day PTS, both sides, percentage threshold 3%
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py --session day --side both --min-abs-pct 3 --min-volume 2000

# Force night PTS, both sides, include ETF/ETN
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py --session night --side both

# Exclude ETF/ETN-like rows when the user asks for individual stocks only
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py --side both --exclude-etf

# Machine-readable output
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py --side both --format json
```

In this Codex desktop environment, live Kabutan fetching normally needs network
escalation. If the user asks for current PTS data, run the helper with
`sandbox_permissions: "require_escalated"` and a concise approval question.

## Pagination Stop Rule

Kabutan sorts these pages by PTS percentage change. Fetch 50-row pages until the
last row crosses the requested threshold:

- Increase pages: stop after the last row is below `+min_abs_pct`.
- Decrease pages: stop after the last row is above `-min_abs_pct`.
- Stop earlier if a page is empty.

Do not assume page 1 is enough unless its final row already crosses the
threshold. Day-session decrease lists can be many pages during broad selloffs.
The volume filter is applied after parsing rows; it does not change the
percentage-based pagination stop rule.

## Cause Analysis Workflow

After ranking:

1. Deduplicate the selected codes across increase/decrease lists.
2. Collect reasons for the selected turnover Top names in a small sequential
   loop. Do not high-frequency fetch Yahoo 掲示板/comments for all names at once.
   Use the natural rhythm: fetch one code, read and summarize the likely reason,
   then move to the next code. Keep moderate randomized sleeps between repeated
   requests to the same host once there are more than three consecutive
   requests, but do not force the user to wait for unnecessary full-list
   scraping before analysis begins.
3. For ordinary stocks, run:

   ```bash
   python3 skills/jp-stock-move-reason/scripts/stock_move_sources.py CODE \
     --format markdown --hours 48 --comments 12 --news-limit 10
   ```

4. For ETF/ETN rows, explain them by the underlying index or strategy instead
   of forcing single-stock news. Examples:
   - Nikkei inverse ETFs rise when Nikkei falls.
   - Nikkei leveraged ETFs fall when Nikkei falls.
   - S&P 500 income/covered-call ETFs may move on the underlying index, FX, and
     thin PTS prints.
5. For rows with very small computed turnover, explicitly mark the reason as
   low-confidence if no concrete news/disclosure exists. Thin PTS prints can
   jump several percent on only 100-300 shares.

## Final Answer Pattern

Report the timestamp, source, and method before the tables:

```text
口径：Kabutan 夜间PTS，YYYY-MM-DD HH:MM JST；
只筛 abs(PTS涨跌幅) >= 3% 且 出来高 > 2,000，
再按 PTS价格 × PTS出来高 算成交额取Top10。
```

Use compact tables:

```text
| 排名 | 代码 | 名称 | PTS涨跌幅 | 成交额 | 原因 |
```

End with a quality note:

- Which names have hard catalysts such as earnings, guidance, buyback, large
  order, lawsuit, capital action, or shareholder benefits.
- Which names are likely thin PTS jumps because turnover is tiny.
- Whether ETF/ETN rows were included or excluded.
