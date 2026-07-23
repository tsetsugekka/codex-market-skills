# Japanese Stock Mover Turnover Ranking Sub-skill

Use this sub-skill when the user asks for current Japanese-stock mover Top10
lists or Kabutan PTS mover lists ranked by trading value / turnover, especially
phrases such as:

- `当前日股涨跌Top10`
- `现在的涨跌榜`
- `PTS夜间涨跌榜成交额Top10`
- `涨跌幅3%以上的成交额top10`
- `不是成交量，是成交额`

## Core Rule

Kabutan mover pages provide price and volume, but not always turnover in the
list view. Compute turnover as:

```text
regular session: computed_turnover = 当前价 * 出来高
PTS session:     computed_turnover = PTS株価 * PTS出来高
```

Default screening is:

```text
abs(騰落率) >= 3%
出来高 > 2000
```

Then rank by `computed_turnover`, not by page order and not by volume alone.

`出来高` is an eligibility filter, not the default ranking key. For generic
requests such as `看看当前涨跌Top10`, `再跑一下PTS`, or colloquial mentions of
`成交量` within this established workflow, preserve turnover ranking. Do not
silently sort by raw volume. Use raw-volume ranking only when the user explicitly
asks for `按出来高排序` or an equivalent unambiguous instruction.

## Sources

Use the rendered/current Kabutan warning pages. Always request 50 rows per page
via the `shared_perpage=50` cookie:

- Regular increase: `https://kabutan.jp/warning/?mode=2_1`
- Regular decrease: `https://kabutan.jp/warning/?mode=2_2`
- Night increase: `https://kabutan.jp/warning/pts_night_price_increase`
- Night decrease: `https://kabutan.jp/warning/pts_night_price_decrease`
- Day increase: `https://kabutan.jp/warning/pts_day_price_increase`
- Day decrease: `https://kabutan.jp/warning/pts_day_price_decrease`

## Section Selection

Default to `--session auto`. The helper selects by JST clock on trading days:

- `09:00-11:30`: use regular increase/decrease pages.
- `11:30-12:30`: use PTS day-section pages.
- `12:30-15:30`: use regular increase/decrease pages.
- `15:30-17:00`: use PTS day-section pages.
- `08:00-09:00`: use PTS day-section pages.
- All other times, weekends, and known non-trading days: use PTS night-section
  pages.

The script handles weekends automatically. If today is a Japanese exchange
holiday on a weekday, pass `--session night` explicitly.

Equivalent routing logic, always evaluated in JST:

```text
if non_trading_day:
    section = pts_night
elif 09:00 <= JST < 11:30 or 12:30 <= JST < 15:30:
    section = regular
elif 08:00 <= JST < 09:00 or 11:30 <= JST < 12:30 or 15:30 <= JST < 17:00:
    section = pts_day
else:
    section = pts_night
```

Treat each boundary as start-inclusive and end-exclusive. For example, `11:30`
switches to PTS day, `12:30` switches back to the regular pages, and `15:30`
switches to PTS day.

For regular pages, the percentage change is against the prior regular close.
For day-session PTS, remember Kabutan compares pre-close prints against the
previous regular-session close and after-close prints against the same-day
regular-session close.

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
# Auto-select regular/PTS day/PTS night section from JST clock
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py --side both

# Force regular market pages
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py --session regular --side both --min-abs-pct 3 --min-volume 2000

# Force PTS day, both sides, percentage threshold 3%
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py --session day --side both --min-abs-pct 3 --min-volume 2000

# Force night PTS, both sides, include ETF/ETN
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py --session night --side both

# Exclude ETF/ETN-like rows when the user asks for individual stocks only
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py --side both --exclude-etf

# Machine-readable output
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py --side both --format json
```

In this Codex desktop environment, live Kabutan fetching normally needs network
escalation. If the user asks for current mover data, run the helper with
`sandbox_permissions: "require_escalated"` and a concise approval question.

## Pagination Stop Rule

Kabutan sorts these pages by percentage change. Fetch 50-row pages until the
last row crosses the requested threshold:

- Increase pages: stop after the last row is below `+min_abs_pct`.
- Decrease pages: stop after the last row is above `-min_abs_pct`.
- Stop earlier if a page is empty.

Do not assume page 1 is enough unless its final row already crosses the
threshold. Day-session decrease lists can be many pages during broad selloffs.
The volume filter is applied after parsing rows; it does not change the
percentage-based pagination stop rule.

## Fetch Discipline

- Request the current Kabutan warning pages with the `shared_perpage=50`
  cookie. Do not use stale `noscript` or SEO fallback content as a live list.
- Add a cache-busting timestamp, parse the page's displayed
  `YYYY年MM月DD日 HH:MM現在` stamp, and report it. Kabutan regular and PTS data
  are normally about 15 minutes delayed, so do not describe them as tick-level
  real time.
- Fetch the complete percentage-qualified range before applying the volume
  filter and turnover sort. Never take the first page or page order as the
  turnover Top10 unless the threshold stop condition proves that it is enough.
- Stop on an empty page and keep a finite page cap. If the host returns rate
  limits, DNS errors, timeouts, resets, or repeated empty responses, report the
  observed failure and stop increasing request frequency.
- Add moderate randomized waits after more than three consecutive requests to
  the same host. Do not parallel-burst Kabutan, Yahoo, or message-board pages.
- Refresh the ranking once before the final answer. If reason collection took
  long enough for membership to change, collect only newly entered codes and
  reuse already verified same-turn reasons for unchanged names.

## Cause Analysis Workflow

After ranking:

1. Deduplicate the selected codes across increase/decrease lists.
2. Unless the user explicitly asks for a raw list only or says reasons are not
   needed, final mover answers must include reasons. Do not stop at a bare
   ranking table.
3. Collect reasons for the selected turnover Top names in a small sequential
   loop using bulk mode. Bulk mode must not access Yahoo at all.
4. For ordinary stocks, run:

   ```bash
   python3 skills/jp-stock-move-reason/scripts/stock_move_sources.py CODE \
     --bulk-reason --format markdown --hours 48 --comments 0 --news-limit 10
   ```

5. `--comments 0` is a hard request-disable switch, not merely an output limit.
   Never run the default single-stock collector for every Top10/Top20 code.
6. Prioritize concrete news, disclosures, earnings, guidance, ratings, orders,
   buybacks, lawsuits, capital actions, or shareholder benefits. Use Yahoo
   掲示板 only as an optional follow-up for at most two stocks whose causes remain
   unclear after the non-Yahoo pass. Wait a randomized 2-4 seconds between those requests.
   On HTTP 403/429, access-denied content, reset, or abnormal empty output, stop
   all Yahoo requests for the rest of the turn; do not retry immediately.
   The collector additionally enforces a shared cross-process randomized 2-4 second Yahoo
   host gap and a 30-minute cooldown after 403/429 or access-control content.
   Never delete or bypass the cooldown for a ranking request.
7. For ETF/ETN rows, explain them by the underlying index or strategy instead
   of forcing single-stock news. Examples:
   - Nikkei inverse ETFs rise when Nikkei falls.
   - Nikkei leveraged ETFs fall when Nikkei falls.
   - S&P 500 income/covered-call ETFs may move on the underlying index, FX, and
     thin PTS prints.
8. For rows with very small computed turnover, explicitly mark the reason as
   low-confidence if no concrete news/disclosure exists. Thin prints can jump
   several percent with little actual capital committed.

## Final Answer Pattern

Report the timestamp, source, and method before the tables. During the regular
cash session use:

```text
口径：Kabutan普通涨跌榜，YYYY-MM-DD HH:MM JST；
只筛 abs(涨跌幅) >= 3% 且 出来高 > 2,000，
再按 当前价 × 出来高 算成交额取Top10。
```

During a PTS session use:

```text
口径：Kabutan 夜间PTS，YYYY-MM-DD HH:MM JST；
只筛 abs(PTS涨跌幅) >= 3% 且 出来高 > 2,000，
再按 PTS价格 × PTS出来高 算成交额取Top10。
```

Use compact tables. During the regular cash session:

```text
上涨 Top10（涨幅大于3%/成交量大于2000/成交额排序）
| 排名 | 代码 | 名称 | 涨跌幅 | 出来高 | 成交额 | 原因 |

下跌 Top10（跌幅大于3%/成交量大于2000/成交额排序）
| 排名 | 代码 | 名称 | 涨跌幅 | 出来高 | 成交额 | 原因 |
```

During PTS sessions:

```text
PTS上涨 Top10（涨幅大于3%/成交量大于2000/成交额排序）
| 排名 | 代码 | 名称 | PTS涨跌幅 | 出来高 | 成交额 | 原因 |

PTS下跌 Top10（跌幅大于3%/成交量大于2000/成交额排序）
| 排名 | 代码 | 名称 | PTS涨跌幅 | 出来高 | 成交额 | 原因 |
```

Use these headings exactly. Report `日中` or `夜间` in the timestamp/method line
below the heading rather than changing the heading text.

Never omit the `原因` column in the final answer unless the user explicitly asks
for numbers only.

End with a quality note:

- Which names have hard catalysts such as earnings, guidance, buyback, large
  order, lawsuit, capital action, or shareholder benefits.
- Which names are likely thin PTS jumps because turnover is tiny.
- Whether ETF/ETN rows were included or excluded.
