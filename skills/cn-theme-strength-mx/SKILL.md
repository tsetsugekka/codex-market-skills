---
name: cn-theme-strength-mx
description: Use when the user asks which A-share themes are rising or falling the most, especially intraday, using an existing /themes stock-theme mapping and 东方财富妙想 MX skills. This skill requires mx-zixuan and mx-xuangu, fetches self-selected-stock quotes first,补抓 missing theme constituents with MX screens, reports live fetch progress, and outputs Top/Bottom theme rankings without writing files by default.
---

# CN Theme Strength MX

Use this skill to rank A-share theme strength from a local `/themes` stock-theme mapping and live or near-live 东方财富妙想 quote data. It is designed for盘中 checks where the user wants to know which themes are strong, which are weak, and how far the fetch has progressed.

## Required Dependencies

This skill must use 东方财富妙想 (`mx`) as the data layer:

- Required: `mx-zixuan` for the first self-selected-stock quote pass.
- Required: `mx-xuangu` for补抓 any `/themes` A-share constituents not returned by `mx-zixuan`.
- Required for default TOP3 driver checks: `mx-search` for current stock/theme资讯.
- Required for default TOP3 driver checks: `cn-stock-move-reason` as the A-share move-reason workflow, but only use its 股吧/讨论-discovery layer for this skill unless the user asks for a full single-stock report.
- Optional: `mx-data` only for follow-up investigation of a specific theme, stock, catalyst, financial metric, or valuation item.

If `mx-zixuan` or `mx-xuangu` is unavailable, unauthenticated, over quota, or missing `MX_APIKEY`, stop and tell the user what is missing. Do not replace this skill's quote layer with non-MX public endpoints. If `mx-search` or `cn-stock-move-reason` is unavailable, still output the ranking, but mark `TOP3 题材驱动检查` as skipped and explain the missing dependency.

## Inputs

Use the existing `/themes` mapping logic whenever available:

- Preferred source: a local `theme-data.json` from the `/themes` project.
- Required row fields: `market`, `code`, `theme`, `weight`.
- Only include `market == "CN"` rows.
- Exclude `theme == "未分類"`.
- Treat repeated stock-theme rows as separate theme memberships.

If no mapping is available in the workspace, ask the user for the theme mapping file or pasteable table. Do not invent the theme universe from MX sector names.

## Fetch Workflow

1. Build the A-share theme universe.
   - Extract unique CN stock codes from the mapping.
   - Keep all CN stock-theme memberships for weighted aggregation.
   - Do not save or print the full stock code list unless the user asks.

2. Query `mx-zixuan` once.
   - Parse `allResults.result.dataList`.
   - Use rows with `SECURITY_CODE`, `SECURITY_SHORT_NAME`, `NEWEST_PRICE`, and `CHG`.
   - Note `total` / `totalRecordCount`, but only trust the returned `dataList`; the self-select API may report more stocks than it returns.
   - Report progress after this pass, for example: `mx-zixuan 返回 200 行，覆盖 /themes A股 172/363，待补抓 191。`

3.补抓 missing `/themes` codes with `mx-xuangu`.
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

Use the same weighted return logic as `/themes`:

```text
theme_return = sum(theme_weight * stock_chg_pct) / sum(theme_weight)
```

Rules:

- Use `CHG` as percentage points, e.g. `10.03` means `+10.03%`.
- A stock that belongs to multiple themes contributes separately to each theme using that row's `weight`.
- For Top themes, choose `主要贡献` stocks by largest positive `weight * CHG`.
- For Bottom themes, choose `主要拖累` stocks by most negative `weight * CHG`.
- Do not output component counts by default.

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
   - Search with the representative stock name/code plus the theme name and likely Chinese aliases when known.
   - Keep only titles/trunks that help explain the theme-level move.
4. Convert stock-level evidence into theme-level inference:
   - Use wording such as `该代表股线索指向...，更像是...题材驱动`.
   - Separate confirmed news from 股吧 speculation.
   - If the stock has an idiosyncratic reason that does not generalize to the theme, say so.

Output this as a compact section after the TOP/BOTTOM tables:

```text
TOP3 题材驱动检查
1. 题材：代表股（代码）...；股吧线索...；mx资讯...；题材推断...
```

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

For `主要贡献` / `主要拖累`, include up to 3 stocks:

```text
三环集团 +16.79%，国瓷材料 +16.54%，风华高科 +10.00%
```

Do not include 成分数 unless the user explicitly asks.

After the tables, output `TOP3 题材驱动检查` using the rules above. Keep it short; this section explains theme movement, not full stock movement.

## Safety

- `mx-zixuan` touches the user's 东方财富 account data. Query self-selected stocks only for this workflow or when the user explicitly asks.
- Never add to, delete from, or modify self-selected stocks unless the user explicitly asks for that mutation.
- Never write `MX_APIKEY`, tokens, cookies, account identifiers, full self-selected lists, raw API responses, private watchlists, or run caches into this public repository.
- Do not expose the full self-selected-stock list in the final answer unless the user asks.
- The output is for market research only and is not investment advice.
