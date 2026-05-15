---
name: stock-technical-analysis
description: Use when the user asks for technical analysis of an individual US, Japanese, or A-share stock, including intraday trend, pressure/support, whether it can reach a price, K-line structure, volume-price behavior, moving averages, KDJ/MACD/RSI, Vegas channels, moomoo/Yahoo chart reads, or whether a breakout/pullback is confirmed.
metadata:
  short-description: Technical analysis playbook for US, JP, and A-share stocks
---

# Stock Technical Analysis

Use this skill when the user asks about price action, technical setup, intraday odds, support/resistance, trend continuation, pullback risk, or chart-based timing for US stocks, Japanese stocks, or A-shares.

This public-safe skill is self-contained and contains only generalized technical-analysis methods. Do not commit personal information, API keys, account data, private RAG files, or any `Stocks` folder contents to GitHub. It must not store personal positions, private research paths, proprietary indicator names, private person names/handles, or private strategy labels. It may use a user-specified private RAG folder during a session, but the skill must remain usable without it.


## Public And Private Versions

If both public and private versions of this skill exist, prefer the private version for local analysis when the user permits it. The private version may use local RAG indexes and user-specific study material.

When updating the skill, keep public and private versions in sync: write public-safe, generalized lessons to the public version; keep private labels, private paths, raw notes, screenshots, account data, and personal trade context only in the private version or private RAG index.

When preparing a GitHub upload or public release, use the public version only and run the release/privacy check in `stock-sentiment-analysis/references/release-and-privacy.md`. Never upload `Stocks/`, private RAG folders, `.ftindex` files, credentials, `.env`, personal data, screenshots, raw PDFs/PPTs, or private strategy labels.

## Core Rule

Before deep analysis, read `references/experience.md` if it exists, but only the `Active Playbook` and `Compression Protocol` sections unless the user explicitly asks for historical lessons. Apply those lessons to intraday execution realism, pressure/support confirmation, and post-discussion learning.

When a live chart is visible in moomoo or another trading/chart app, use the chart directly if the user asks for `现在`, `再看看`, `moomoo`, `分时`, `图表`, `资金流`, `盘口`, or asks whether a level is being confirmed. Confirm the ticker and chart timeframe before reading signals.

Never answer only by following the latest tick. Use the sequence:

1. Determine the timeframe: intraday trade, 1h+ swing, trend holding, or post-event reaction. For 1h+ and swing judgments, combine technicals with sentiment/news context instead of reading the chart alone.
2. Read price location: current price versus prior high/low, opening price, yesterday close, VWAP if available, 5/20-day lines, and obvious pressure/support.
3. Check volume-price confirmation: breakout must show volume and stand above the level; volume without price progress is possible distribution; shrinking pullback can be healthy only if support holds.
4. Check momentum: KDJ, MACD, RSI, and whether price makes a new high while momentum does not.
5. Check structure: trend continuation, high-level divergence, 空中加油, 回踩确认, 破位反抽, or 冲高回落.
6. Check market context: sector/peer confirmation, broad market tone, rates/FX/volatility when relevant, and for A-shares the emotion cycle. Use `stock-sentiment-analysis` for a deeper shared sentiment framework.
7. Give conditional conclusions rather than one-point predictions.

If a long multi-turn discussion about one stock produces a verified reusable lesson, update `references/experience.md` after answering. Generalize the lesson; do not store ticker-specific notes as the main content.

Do not read local research folders or indicator files by default. If the user explicitly provides a file or asks to learn from a specific document, extract only reusable public-safe rules. Do not store local file paths, proprietary indicator names, personal slogans, private strategy names, private person names/handles, or original document labels in this skill. Generic public concepts such as Vegas channels, KDJ, MACD, RSI, VWAP, and support/resistance may be retained.

## Optional User Knowledge Base

If a user wants to use their own study materials, ask them to specify a private RAG or index folder outside this public repository. Raw PDFs, screenshots, indicators, notes, and private labels should stay private. Offer to create or update a lightweight local index for repeated use, with only user-approved aliases, topics, page/slide ranges, keywords, and public-safe summaries. Only distilled, generic rules should be copied into `references/experience.md` or `references/stocks-technical-playbook.md`, and only when the user explicitly asks to update the skill. Do not write the private path, private labels, or raw source text into public files. The skill must remain usable without that private corpus.

## When To Load The Reference

For quick answers, apply the core rule directly.

For any of the following, read `references/stocks-technical-playbook.md` first:

- The user asks "能不能到某个价格", "现在怎么看", "日内", "分时", "压力位", "支撑位", "技术分析", "买点", "卖点", "突破", "回踩", "空中加油", "KDJ", "MACD", "RSI", or "Vegas".
- The stock has already moved sharply today.
- The answer may affect a same-day trading decision.
- You are using moomoo, Yahoo chart, or screenshots to read the chart.
- The user asks to use moomoo or another charting/trading app, or the chart is already visible and current.

If the user asks for a post-mortem, review, or lesson update after the stock moves as discussed, read and update `references/experience.md` first, then edit references only if a core checklist needs to change.

For chart-app workflows, read the `Chart App Visual Workflow` section in `references/stocks-technical-playbook.md`.

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
- US option gamma: `us-stock-gamma-moomoo`

For US stocks, choose based on the question: use `us-stock-gamma-moomoo` when option positioning, gamma walls, 0DTE, IV, or dealer hedging matter; use this skill when chart structure and timing matter; use both when an options map needs price-action confirmation.

When both fundamentals/catalysts and technicals matter, gather source evidence first, then use this skill to judge whether the chart confirms, overextends, or contradicts the story.
