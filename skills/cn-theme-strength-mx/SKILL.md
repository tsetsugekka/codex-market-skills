---
name: cn-theme-strength-mx
description: Use by default when the user asks to check A-share theme strength, current A-share themes, theme rankings, which themes are strongest/weakest, or which themes are rising/falling most, especially intraday. Uses a local A-share stock-theme mapping cache and 东方财富妙想 MX skills. This skill requires mx-zixuan and mx-xuangu, fetches self-selected-stock quotes first,补抓 missing theme constituents with MX screens, reports live fetch progress, and outputs Top/Bottom theme rankings without writing files by default.
---

# CN Theme Strength MX

Use this skill to rank A-share theme strength from the local A-share stock-theme mapping cache and live or near-live 东方财富妙想 quote data. It is designed for盘中 checks where the user wants to know which themes are strong, which are weak, and how far the fetch has progressed.

## Routing: Fast Board Tape vs Formal Theme Strength

Default to this skill when the user asks in Chinese or English for `题材强弱`, `当前A股题材`, `题材排序`, `强题材`, `弱题材`, `theme strength`, or similar wording. In this context, `题材` means the local custom theme universe plus MX constituent quotes, not a generic broker board list.

## Reference Reading Rule

When this skill selects a reference file, read the complete file before applying it. Do not rely on a partial excerpt, heading-only scan, or stale memory of the reference.

Use a fast market-board ranking source such as 东方财富 concept/industry board rankings only when the user explicitly asks for `快速看盘面`, `板块榜`, `行业/概念板块排行`, `现在市场炒什么`, or a quick broad tape read. That fast board-tape result may be useful as an auxiliary confirmation layer, but it is not this skill's formal theme-strength output.

When both views are useful, run this skill first for the formal conclusion, then optionally compare it with fast board rankings and explain differences in口径. If the answer uses this skill, state that the result is based on the local custom theme mapping and MX constituent-weighted returns, not directly on 东方财富 concept/industry board涨跌幅.

## Required Dependencies

This skill must use 东方财富妙想 (`mx`) as the data layer:

- Required: `mx-zixuan` for the first self-selected-stock quote pass.
- Required: `mx-xuangu` for补抓 any local-mapping A-share constituents not returned by `mx-zixuan`.
- Required for default TOP3 driver checks: `mx-search` for current stock/theme资讯.
- Required for default TOP3 driver checks: `cn-stock-move-reason` as the A-share move-reason workflow, but only use its 股吧/讨论-discovery layer for this skill unless the user asks for a full single-stock report.
- Optional: `mx-data` only for follow-up investigation of a specific theme, stock, catalyst, financial metric, or valuation item.

If `mx-zixuan` or `mx-xuangu` is unavailable, unauthenticated, over quota, or missing `MX_APIKEY`, stop and tell the user what is missing. Do not replace this skill's quote layer with non-MX public endpoints. If `mx-search` or `cn-stock-move-reason` is unavailable, still output the ranking, but mark `TOP3 题材驱动检查` as skipped and explain the missing dependency.

## Local Theme Cache

This skill uses two local cache files under `assets/themes/` when available:

- `assets/themes/theme-data.json`: stock-theme memberships.
- `assets/themes/theme-label-i18n.json`: display labels; use each theme's `zh` value for Chinese output.

The optional online refresh source is DayTrading.monster. The refresh script downloads only these two files:

- `https://daytrading.monster/themes/theme-data.json`
- `https://daytrading.monster/themes/theme-label-i18n.json`

Do not fetch `theme-material-i18n.json` or `theme-quotes.json` for this skill. Theme material is not needed for the ranking workflow, and quote data must still come from MX during the current run.

At the start of a normal theme-strength run, try this local refresh command once. It creates the cache if either file is missing, and skips network access when both files are valid and fresher than 7 days:

```bash
python3 <cn-theme-strength-mx>/scripts/refresh_theme_assets_from_daytrading_monster.py
```

If network access fails but the local cache files are valid, continue with the existing local cache and state that the mapping refresh was skipped. If the cache files are missing or invalid and refresh fails, ask the user for local mapping files instead of inventing the theme universe. If the user explicitly provides a newer local theme-mapping path, use that path for the current run, but do not write the user's local data back to the repository unless the user explicitly asks to update a local cache.

When manually updating the local cache from a local source directory, this copy script is still available:

```bash
python3 skills/cn-theme-strength-mx/scripts/refresh_theme_assets.py /path/to/public-theme-source
```

Use the local mapping logic:

- Preferred source: local `assets/themes/theme-data.json`, refreshing it first when missing or stale.
- Preferred Chinese label source: local `assets/themes/theme-label-i18n.json`, refreshing it first when missing or stale.
- `theme-data.json` is expected to contain `rows[]`; if a user-provided file is a plain list, treat that list as rows.
- Required row fields: `market`, `code`, `theme`, `weight`.
- Only include `market == "CN"` rows.
- Exclude `theme == "未分類"`.
- Treat repeated stock-theme rows as separate theme memberships.
- Keep the original `theme` key internally for joins and aggregation, but display the Chinese label in all user-facing tables and driver checks.
- If a Chinese label is missing, fall back to the original theme name and mention the missing label only when it affects visible output.

If the local mapping files are missing or invalid and cannot be refreshed, stop and ask the user for either:

- a local path to `theme-data.json` plus `theme-label-i18n.json`; or
- a pasteable table with at least `market`, `code`, `theme`, `weight`, and optionally Chinese labels.

Do not invent the theme universe from MX sector names.

## Fetch Workflow

1. Build the A-share theme universe.
   - Extract unique CN stock codes from the mapping.
   - Keep all CN stock-theme memberships for weighted aggregation.
   - Do not save or print the full stock code list unless the user asks.

2. Query `mx-zixuan` once.
   - Parse `allResults.result.dataList`.
   - Use rows with `SECURITY_CODE`, `SECURITY_SHORT_NAME`, `NEWEST_PRICE`, and `CHG`.
   - Note `total` / `totalRecordCount`, but only trust the returned `dataList`; the self-select API may report more stocks than it returns.
   - Report progress after this pass, for example: `mx-zixuan 返回 200 行，覆盖内置映射 A股 172/363，待补抓 191。`

3.补抓 missing local-mapping codes with `mx-xuangu`.
   - Batch missing codes in groups of at most 50.
   - Use a query shaped like:

```text
股票代码为002131、600986、603258的A股，返回代码、名称、最新价、涨跌幅
```

   - Run batches serially by default. Do not fire many MX requests in parallel; it can trigger `操作过于频繁`.
   - After each batch, report progress: completed batch count, returned row count, remaining codes.
   - Validate `responseCode == "100"` and that returned rows cover the requested codes.
   - If MX returns `操作过于频繁` / `503`, wait 8-15 seconds and retry the same batch. Retry up to 2 times unless the user asks to keep trying.
   - If a few codes remain missing after retries, list only the missing code count and a short sample, then continue ranking from available data while clearly marking incompleteness.

4. Merge quotes.
   - Prefer `mx-zixuan` quotes for codes it returned.
   - Use `mx-xuangu` rows only for missing codes.
   - If dates differ across sources, prefer the latest date only if it is internally consistent; otherwise warn that the mixed-date result is not clean.
   - Read the quote date from MX column `dateMsg`. During weekends or market holidays, state that the data is from the latest available trading day.

## Aggregation

Use the same weighted return logic as the local mapping:

```text
theme_return = sum(theme_weight * stock_chg_pct) / sum(theme_weight)
```

Rules:

- Use `CHG` as percentage points, e.g. `10.03` means `+10.03%`.
- A stock that belongs to multiple themes contributes separately to each theme using that row's `weight`.
- Rank by the original local theme key, but render labels through `theme-label-i18n.json[theme].zh`.
- For Top themes, choose `主要贡献` stocks by largest positive `weight * CHG`.
- For Bottom themes, choose `主要拖累` stocks by most negative `weight * CHG`.
- Do not output component counts by default.

## Theme Lifecycle Lens

When the user asks which themes are true mainlines, whether a strong theme can continue, or whether today's strength is only rotation/noise, read `references/theme-mainline-lifecycle.md` and apply it after the ranking. Do not replace the weighted-return ranking with this lens; use it only to interpret durability, crowding, and follow-through quality.

For default TOP3 driver checks, use the lifecycle lens lightly: identify whether each top theme looks like early emergence, acceleration, climax/divergence, old-leader rebound, defensive substitute, or one-day noise when the available evidence supports that classification. If evidence is insufficient, say `周期位置暂不确认`.

## TOP3 Driver Check

After ranking, inspect only the top 3 themes. The goal is not to analyze the selected stock itself; it is to infer why the theme moved by looking at the strongest representative stock's discussion and news.

For each TOP3 theme:

1. Select one representative stock:
   - Choose the stock with the highest `CHG` inside that theme.
   - If tied, choose the higher `weight * CHG` contributor.
2. Use `cn-stock-move-reason` only as a 股吧/讨论 discovery workflow:
   - Do not run a full single-stock report unless the user asks.
   - Limit the evidence to recent 股吧/资讯 discussion snippets or topic clues that explain what traders think is driving the move.
   - Do not use its full announcement, market-context, technical, or emotion-cycle output for this default theme-ranking workflow.
3. Use `mx-search` for current资讯:
   - Search with the representative stock name/code plus the Chinese theme label and likely Chinese aliases when known.
   - Keep only titles/trunks that help explain the theme-level move.
4. Convert stock-level evidence into theme-level inference:
   - Use wording such as `该代表股线索指向...，更像是...题材驱动`.
   - Separate confirmed news from 股吧 speculation.
   - If the stock has an idiosyncratic reason that does not generalize to the theme, say so.
   - Assign a compact confidence label:
     - `较高`: 股吧/资讯 and `mx-search` both point to the same sector-level driver, and several theme constituents also rose.
     - `中等`: `mx-search` supports the sector driver, but 股吧 discussion is noisy or representative-stock specific.
     - `较低`: evidence is mostly 股吧 speculation, stale news, overseas sympathy, or an idiosyncratic stock reason.

Output this as a compact section after the TOP/BOTTOM tables:

```text
TOP3 题材驱动检查
1. 题材：代表股（代码，涨跌幅）。股吧线索：...；mx资讯：...；题材推断：...；确定度：较高/中等/较低。
```

Example style:

```text
1. MLCC・ケミコン：三环集团（300408，+16.79%）。股吧线索集中在 MLCC、AI服务器、英伟达需求和国产替代；mx资讯指向英伟达 Rubin / AI数据中心带动高端 MLCC 用量上升、供给紧张和涨价潮。题材推断：更像是 AI服务器高端 MLCC 需求 + 涨价 + 国产替代共振。确定度：较高。
```

Keep each item to 2-4 sentences. This section should explain the theme driver, not repeat the whole representative stock report.

## Output Style

Reply in Chinese unless the user asks otherwise. Do not write output files by default.

Start with a compact status line:

```text
数据日期：2026.05.22；抓取：mx-zixuan 200行，mx-xuangu补抓4批，363/363代码齐全。
```

Then output two tables:

1. `TOP10`
2. `BOTTOM10`

Default table columns:

```text
排名 | 题材 | 加权涨跌幅 | 主要贡献
排名 | 题材 | 加权涨跌幅 | 主要拖累
```

`题材` must use the local Chinese theme label. Do not show Japanese theme names in the final answer when a `zh` label exists.

For `主要贡献` / `主要拖累`, include up to 3 stocks:

```text
三环集团 +16.79%，国瓷材料 +16.54%，风华高科 +10.00%
```

Do not include 成分数 unless the user explicitly asks.

After the tables, output `TOP3 题材驱动检查` using the rules above. Keep it short; this section explains theme movement, not full stock movement. The expected fields are `代表股`, `股吧线索`, `mx资讯`, `题材推断`, and `确定度`.

## Safety

- `mx-zixuan` touches the user's 东方财富 account data. Query self-selected stocks only for this workflow or when the user explicitly asks.
- Never add to, delete from, or modify self-selected stocks unless the user explicitly asks for that mutation.
- Never write `MX_APIKEY`, tokens, cookies, account identifiers, full self-selected lists, raw API responses, private watchlists, or run caches into this public repository.
- Do not expose the full self-selected-stock list in the final answer unless the user asks.
- The output is for market research only and is not investment advice.
