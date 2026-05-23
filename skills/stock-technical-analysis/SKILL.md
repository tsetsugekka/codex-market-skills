---
name: stock-technical-analysis
description: Use when the user asks for technical analysis of an individual US, Japanese, or A-share stock, including intraday trend, pressure/support, whether it can reach a price, K-line structure, volume-price behavior, moving averages, KDJ/MACD/RSI, Vegas channels, moomoo/Yahoo chart reads, US-only dark-pool level confirmation, or whether a breakout/pullback is confirmed.
metadata:
  short-description: Technical analysis playbook for US, JP, and A-share stocks
---

# Stock Technical Analysis

Use this skill when the user asks about price action, technical setup, intraday odds, support/resistance, trend continuation, pullback risk, or chart-based timing for US stocks, Japanese stocks, or A-shares.

This public-safe skill is self-contained and contains only generalized technical-analysis methods. Do not commit personal information, API keys, account data, private RAG files, or private research materials to GitHub. It must not store personal positions, private research paths, proprietary indicator names, private person names/handles, or private strategy labels. It may use a user-specified private RAG folder during a session, but the skill must remain usable without it.


## Public And Private Versions

If both public and private versions of this skill exist, prefer the private version for local analysis when the user permits it. The private version may use local RAG indexes and user-specific study material.

When updating the skill, keep public and private versions in sync: write public-safe, generalized lessons to the public version; keep private labels, private paths, raw notes, screenshots, account data, and personal trade context only in the private version or private RAG index.

When preparing a GitHub upload or public release, use the public version only and run the repo-level release/privacy check from the repository root at `shared/references/release-and-privacy.md`. Never upload private RAG folders, `.ftindex` files, credentials, `.env`, personal data, screenshots, raw PDFs/PPTs, or private strategy labels.

## Core Rule

Before deep analysis, read `references/experience.md` if it exists, but only the `Active Playbook` and `Compression Protocol` sections unless the user explicitly asks for historical lessons. Apply those lessons to intraday execution realism, pressure/support confirmation, and post-discussion learning.

Cross-skill calls are operational. When this workflow says to use another market skill, actually load that skill's `SKILL.md` and required references if the skill is installed or available as a sibling in this repository. Do not merely mention the other skill by name in the answer.

When a live chart is visible in moomoo or another trading/chart app, use the chart directly if the user asks for `现在`, `再看看`, `moomoo`, `分时`, `图表`, `资金流`, `盘口`, or asks whether a level is being confirmed. Confirm the ticker and chart timeframe before reading signals.

For U.S. stocks and ETFs, prefer direct moomoo OpenD 1-minute K-line data over screenshot-only reads when OpenD is available. Subscribe to `SubType.K_1M` first, then call `get_cur_kline`; if the subscription fails because of missing permissions, unsupported symbols, or index restrictions, fall back to the moomoo app chart or a user-provided screenshot. OpenD may not support U.S. index K-lines such as `.SPX`, and some local setups may not have Japanese-stock or A-share permissions, so use SPY or the relevant ETF as a proxy only when appropriate and state the proxy clearly. When using SPY to judge SPX intraday structure, convert SPY levels into SPX levels before answering, using the freshest SPX or ES/SPX anchor available; report SPX levels first and note the SPY proxy only as source context.

Never answer only by following the latest tick. Use the sequence:

1. Determine the timeframe: intraday trade, 1h+ swing, trend holding, or post-event reaction. For 1h+ and swing judgments, combine technicals with sentiment/news context instead of reading the chart alone.
2. Read price location: current price versus prior high/low, opening price, yesterday close, VWAP if available, 5/20-day lines, and obvious pressure/support.
3. Check volume-price confirmation: breakout must show volume and stand above the level; volume without price progress is possible distribution; shrinking pullback can be healthy only if support holds.
4. Check momentum: KDJ, MACD, RSI, and whether price makes a new high while momentum does not.
5. Check structure: trend continuation, high-level divergence, 空中加油, 回踩确认, 破位反抽, or 冲高回落.
6. For U.S.-listed stocks/ETFs only, optionally use ChartExchange dark-pool/off-exchange levels as hidden-liquidity reference zones when the stock has unusual volume, unexplained movement, repeated support/resistance, or a news reaction that price is accepting/rejecting. Do not apply this to A-shares or Japanese stocks. Dark-pool data has no buy/sell side; a level matters technically only after price confirms it with acceptance, rejection, repeated defense, or failure to reclaim.
7. Check market context: sector/peer confirmation, broad market tone, rates/FX/volatility when relevant, and for A-shares the emotion cycle. Call `macro-news-check` only when current macro or broad-market tape can plausibly change the read, such as index-wide selloffs/squeezes, rates/FX shocks, central-bank or data releases, commodities, geopolitics, or sudden futures moves. Use `stock-sentiment-analysis` for a deeper shared sentiment framework.
8. Give conditional conclusions rather than one-point predictions.

For A-share technical reads, optionally use 东方财富妙想 skills when they are already installed, but keep them as a supplemental data layer rather than a replacement for the existing price-action workflow. Continue to judge trend, support/resistance, volume-price confirmation, sector/broad-market context, sentiment, and macro when relevant. `mx-data` can supplement current quote,涨跌幅,成交额/量,主力资金, historical prices, index/sector context, and valuation fields; `mx-search` can supplement current event/news context when a technical break may be news-driven; `mx-xuangu` can help build peer or board constituent comparisons and can run natural-language technical screens such as consecutive moving-average alignment plus price-above/below-MA conditions. If the user asks which A-shares belong to a sector/theme or asks for `相关股`, `概念股`, `龙头股`, or `板块成分`, use `mx-xuangu` first when available. Do not block the analysis if these skills are unavailable or fail; you may briefly suggest installing/configuring 妙想 only when that layer would materially improve the exact A-share request. Use `mx-zixuan` and `mx-moni` only when the user explicitly asks for self-selected-stock management/filtering or simulated portfolio/trade operations.

If a long multi-turn discussion about one stock produces a verified reusable lesson, update `references/experience.md` after answering. Generalize the lesson; do not store ticker-specific notes as the main content.

Do not read local research folders or indicator files by default. If the user explicitly provides a file or asks to learn from a specific document, extract only reusable public-safe rules. Do not store local file paths, proprietary indicator names, personal slogans, private strategy names, private person names/handles, or original document labels in this skill. Generic public concepts such as Vegas channels, KDJ, MACD, RSI, VWAP, and support/resistance may be retained.

## Optional User Knowledge Base

If a user wants to use their own study materials, ask them to specify a private RAG or index folder outside this public repository. Raw PDFs, screenshots, indicators, notes, and private labels should stay private. Offer to create or update a lightweight local index for repeated use, with only user-approved aliases, topics, page/slide ranges, keywords, and public-safe summaries. Only distilled, generic rules should be copied into `references/experience.md` or `references/technical-playbook.md`, and only when the user explicitly asks to update the skill. Do not write the private path, private labels, or raw source text into public files. The skill must remain usable without that private corpus.

## When To Load The Reference

For quick answers, apply the core rule directly.

For any of the following, read `references/technical-playbook.md` first:

- The user asks "能不能到某个价格", "现在怎么看", "日内", "分时", "压力位", "支撑位", "技术分析", "买点", "卖点", "突破", "回踩", "空中加油", "KDJ", "MACD", "RSI", or "Vegas".
- The stock has already moved sharply today.
- The answer may affect a same-day trading decision.
- You are using moomoo, Yahoo chart, or screenshots to read the chart.
- The user asks to use moomoo or another charting/trading app, or the chart is already visible and current.

If the user asks for a post-mortem, review, or lesson update after the stock moves as discussed, read and update `references/experience.md` first, then edit references only if a core checklist needs to change.

For chart-app workflows, read the `Chart App Visual Workflow` section in `references/technical-playbook.md`.

For Japanese stocks and A-shares, prefer `jp-stock-move-reason` or `cn-stock-move-reason` as the first pass for news/emotion/catalyst context. Use this skill after that first pass when the user asks for chart timing, when the discussion becomes repeated/deeper, or when a 1h+ chart must confirm whether the narrative is accepted.

## Output Style

Reply in Chinese unless the user asks otherwise. Be decisive but conditional.

Use this compact structure when useful:

1. `结论`: state whether the setup is strong, weak, or only a candidate, and name the key confirmation level.
2. `技术结构`: trend, support/resistance, moving averages, and K-line pattern.
3. `量价/动能`: volume, KDJ/MACD/RSI, divergence, and funding/order-flow clues if available.
4. `触发条件`: what must happen for the bullish or bearish scenario to confirm.
5. `失效条件`: the level or signal that invalidates the read.

Avoid giving direct trading instructions. Use probability bands only when the evidence supports them, and explain what would change the probability.

## Coordination With Market Skills

This skill handles chart and technical structure. For catalysts, valuation, news, 掲示板/股吧, and move reasons, combine it with the relevant market skill:

- Japanese stocks: `jp-stock-move-reason`
- A-shares: `cn-stock-move-reason`
- Shared emotion framework: `stock-sentiment-analysis`
- Macro and broad-market tape when needed: `macro-news-check`
- US option gamma: `us-stock-gamma-moomoo`

For US stocks, choose based on the question: use `us-stock-gamma-moomoo` when option positioning, gamma walls, 0DTE, IV, or dealer hedging matter; use this skill when chart structure and timing matter; use both when an options map needs price-action confirmation.

For U.S. dark-pool technical confirmation, use ChartExchange or FINRA-derived pages only as a secondary layer. Construct ChartExchange URLs from the actual listing venue and ticker, such as `nyse-anet`, `nasdaq-nvda`, or `nyse-spy`; SPY commonly resolves to `nyse-spy` on ChartExchange. If the listing venue is unknown, search the ticker first instead of reusing a prior URL. Treat high-volume dark-pool levels like unconfirmed support/resistance until price/VWAP/volume confirms them.

When both fundamentals/catalysts and technicals matter, gather source evidence first, then use this skill to judge whether the chart confirms, overextends, or contradicts the story.
