---
name: market-daily-strategist
description: Use when the user asks for Chinese market strategy reports or long-term stock recommendations covering US stocks, Japanese stocks, or A-shares, including pre-market strategy, close recap, and one-name long-term recommendation reports. Applies to ad-hoc requests that need live market/news data, strict no-fabrication data discipline, price-confirmed catalysts, and decision-oriented trading guidance.
metadata:
  short-description: Chinese daily market strategy and one-stock recommendation reports
---

# Market Daily Strategist

Use this skill for the user's market reports. This is not a scheduler; ignore any clock-trigger wording from the original prompts. Route by user intent:

- 美股盘前、开盘前、pre-market、盘前策略: read `references/us-pre-market.md`.
- 美股收盘、昨晚美股、复盘、close recap: read `references/us-close-briefing.md`.
- 日股盘前、日经盘前、日本开盘前: read `references/jp-pre-market.md`.
- 日股收盘、今天日股复盘、日本市场复盘: read `references/jp-close-briefing.md`.
- A股盘前、A股早盘、开盘前策略: read `references/cn-pre-market.md`.
- A股收盘、A股复盘、今天A股市场回顾: read `references/cn-close-briefing.md`.
- 美股长线推荐、推荐一只美股: read `references/us-long-term.md`.
- 日股长线推荐、推荐一只日股: read `references/jp-long-term.md`.
- A股长线推荐、推荐一只A股/ETF/LOF: read `references/cn-long-term.md`.

If the user says only `盘前信息`, `收盘复盘`, or `推荐一只股票`, infer the market from the conversation. If unclear, ask one concise question for the market: 美股、日股、还是A股.

Always read `references/shared.md` first, then only the one task-specific reference that matches the user request.

Reference reading rule: when this skill selects a reference file, read the complete file before applying it. Do not rely on a partial excerpt, heading-only scan, or stale memory of the reference.

When the user asks about medium/long-term market direction, cross-market strategy, market regime, bull/bear structure, or the durability of a theme-driven rally, also read `references/global-mainline-funds-game-cycle.md`.

## Core Workflow

1. Identify the report type and market.
2. Confirm current date/time in Japan time and whether the relevant next or current session is open. If the market is closed, follow the task-specific closed-market rule instead of forcing a normal report.
3. Gather latest data from reliable live sources. Use market-specific primary sources listed in the task reference.
4. Never invent prices, index levels, futures, percentage moves, gamma/options levels, flows, valuation, financials, or news. If unavailable, say `暂无具体数值` or `初步`.
5. Apply `shared.md` market-news and local-data discipline: scan enough current news before finalizing, avoid broad local-data sweeps, and prioritize items confirmed by price action, volume, flows, earnings, ratings, policy catalysts, or direct trading relevance.
6. Produce pure simplified Chinese output in the exact structure required by the task reference.

## Supporting Skills

This skill is a report router and synthesis layer. Use other market skills when they materially improve the report, but keep calls selective.

- Use `macro-news-check` when the report depends on current macro tape: rates, FX, oil, gold, commodities, central banks, economic data, geopolitics, broad risk sentiment, or live futures confirmation.
- For U.S. reports, use official moomoo skills as selective evidence helpers when installed: `moomoo-news-search` and `moomoo-stock-digest` for timely company/news context, `moomoo-comment-sentiment` for community heat, `moomoo-capital-anomaly` for capital-flow anomalies, `moomoo-derivatives-anomaly` for U.S.-applicable option anomaly dimensions, and `moomoo-technical-anomaly` for a first-pass technical anomaly scan. These are data and anomaly layers; keep this skill responsible for strategy synthesis.
- Use `us-stock-move-reason` for 1-3 important U.S. movers when the catalyst, earnings/guidance acceptance, news interpretation, option/flow anomaly, or community reaction needs a dedicated move-reason pass.
- Use `us-stock-gamma-moomoo` for US index/ETF option structure when SPX/SPY/QQQ/NQ gamma, GEX, 0DTE, dealer positioning, option walls, or intraday conversion levels could change the strategy.
- Use `stock-technical-analysis` for selected index/ETF/stock levels when the answer needs support/resistance, trend confirmation, intraday execution timing, breakout/pullback validation, or stop levels.
- Use `jp-stock-move-reason` or `cn-stock-move-reason` for 1-3 genuinely important Japanese/A-share movers when the catalyst is unclear or the stock drives the day's theme. Do not run move-reason analysis on every mover.
- Use `stock-sentiment-analysis` when crowding, leader/follower status, emotion cycle, old-leader rebound, or theme acceptance/rejection affects the trading conclusion.
- Use 东方财富妙想 skills for A-share reports and sector questions when available, as supplemental data/search/screening only. They do not replace the report's existing market-news discipline, price-confirmed catalyst checks, emotion-cycle and leader/follower judgment, macro/technical confirmation, or source hierarchy. Use `mx-data` for quote, valuation, fund-flow, financials, index/sector data; `mx-search` for timely news, announcements, research, policy, and event explanations; `mx-xuangu` for sector/concept constituents, related-stock lists, condition screens, and peer comparisons. For questions like `A股某板块有哪些股票`, `相关股`, `概念股`, `龙头股`, or `板块成分`, try `mx-xuangu` first when available. Use `mx-zixuan` only when the user explicitly asks about 东方财富 self-selected stocks, and `mx-moni` only for explicit simulated-trading tasks.

Cross-skill calls are operational: actually load the supporting skill's `SKILL.md` and required references when using it. Keep supporting-skill output compressed into the final report instead of pasting separate mini-reports.

## Style

- Professional, concise, strategy-first.
- The first line is always a 60-80 Chinese-character decisive title when the task reference requires it.
- Prioritize actionable conclusions: 追高、等回踩、低吸、减仓、观察、避开财报风险、仓位与止损.
- Attribute important live figures and news to sources.
- For recommendation reports, clearly state that the output is not financial advice.

## Guardrails

- Do not open or depend on the DTM `/themes` project or `https://daytrading.monster/themes/` unless the user explicitly asks to update or inspect that project.
- For long-term recommendation reports, recommend exactly one target and avoid recently recommended names when that history is available in the conversation, logs, or user-provided context.
- Buy prices must be near the latest available price and within the task-specific limit, generally no more than 2% above current/latest price.
