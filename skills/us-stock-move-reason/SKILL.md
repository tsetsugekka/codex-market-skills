---
name: us-stock-move-reason
description: Use when analyzing why a U.S. stock or ETF moved sharply, including premarket/after-hours gaps, earnings reactions, guidance, ratings, company news, unusual options, capital-flow anomalies, short data, community sentiment, and technical confirmation. Coordinates official moomoo skills and local market skills into a Chinese evidence-based move-reason note.
metadata:
  short-description: Analyze U.S. stock move reasons from moomoo news, anomalies, sentiment, options, and technical context
---

# US Stock Move Reason

Use this skill as the U.S. stock counterpart to `jp-stock-move-reason` and `cn-stock-move-reason`. It is an evidence-gathering and synthesis workflow, not a trading bot.

This public-safe skill must not store account data, OpenD logs, API keys, cookies, private RAG paths, personal positions, screenshots, raw private notes, or proprietary labels. It may call official moomoo skills when installed, but those skills remain external data/anomaly providers.

## Workflow

1. Normalize the target into a U.S. market symbol such as `US.NVDA`, `US.DELL`, `US.SPY`, or `US.TSLA`. If the user gives only a name and the listing is ambiguous, ask one concise question. Treat broad index questions (`SPX`, `SPY`, `QQQ`, `NQ`) as U.S. index/ETF workflows and consider `macro-news-check` by default.

2. Establish whether the move is real:
   - Use `moomooapi` when available for snapshot, premarket/after-hours fields, daily or 1-minute K-line context, volume, turnover, market state, and basic stock information.
   - If OpenD or permissions fail, use public quote sources only as fallback and state the limitation.
   - For SPX, moomoo may reject `US..SPX` index snapshots while still allowing SPX/SPXW option chains. Use `SPY`, ES/CFD, or user-provided SPX anchors when needed and state the anchor.

3. Gather confirmed catalysts first:
   - Use `moomoo-news-search` or `moomoo-stock-digest` for current company news, earnings, guidance, ratings, orders, regulatory events, M&A, capital actions, analyst notes, and sector read-through.
   - When earnings are involved, apply expectation gap explicitly: `prior market expectation` -> `actual result / guidance / commentary` -> `above expectation`, `in line or merely landed`, or `below expectation`.
   - Do not let social posts, option prints, or technical signals replace confirmed filings/news.

4. Scan official moomoo anomaly layers when they are installed and relevant:
   - `moomoo-capital-anomaly`: use for capital-flow, broker, short-sale, or funds-flow anomaly requests. A `无异常` response is a usable result.
   - `moomoo-derivatives-anomaly`: use for U.S.-applicable option dimensions only: `option_unusual`, `option_volatility`, `option_volume_price`, `option_sentiment`, and `option_comprehensive`. Do not request Hong Kong warrant / CBBC dimensions for U.S. stocks. If a full scan returns an opaque backend error, retry with explicit U.S. option dimensions before concluding the skill is unavailable.
   - `moomoo-technical-anomaly`: use as a first-pass technical anomaly scanner, then verify with `stock-technical-analysis`.
   - `moomoo-comment-sentiment`: use for moomoo community heat, disagreement, chasing, panic, and representative viewpoints. Label it as a moomoo community sample, not a full-market sentiment survey.

5. Add supporting skills based on what the evidence shows:
   - Use `us-stock-gamma-moomoo` when options positioning, gamma walls, 0DTE, IV, SPX/SPY/QQQ, or dealer hedging can change the interpretation.
   - Use `stock-technical-analysis` when support/resistance, trend confirmation, failed breakout, VWAP, 1-minute K-lines, or intraday timing matter.
   - Use `stock-sentiment-analysis` when crowding, leader/follower status, risk-on/risk-off psychology, expectation reset, or social/community emotion changes the conclusion.
   - Use `macro-news-check` when Fed, rates, yields, USD, oil/gold, index futures, economic data, geopolitics, or broad market tape may be the main driver or amplifier.

6. Evidence priority:
   - Confirmed company news, filings, earnings, guidance, ratings, and direct disclosures.
   - Current quote, volume, gap, market state, and price acceptance/rejection.
   - Sector/peer and broad market context.
   - Option, capital-flow, short, and technical anomaly scans.
   - Community sentiment and social posts as secondary psychology evidence only.

## Output Style

Reply in Chinese unless the user asks otherwise. For every stock analyzed, use these six numbered sections in this exact order:

1. `最有力理由`: the most likely catalyst, source type, and expectation gap.
2. `补助理由`: sector/peer, macro, positioning, valuation, short/flow, or liquidity drivers.
3. `期权/资金/技术异动`: summarize only relevant moomoo anomaly and gamma/technical evidence; say `无异常` when a checked layer returns no anomaly.
4. `社区情绪`: moomoo community or other forum/social heat, representative views, and sample limitations.
5. `确定度`: high / medium / low, with one sentence explaining why.
6. `注意点`: what is unconfirmed, what could invalidate the read, and what needs a fresh check.

When evidence is thin, say so. Use `思惑`, `未确认`, or `确认待ち` for claims that appear only in community posts or option-flow interpretation. Do not give direct trading instructions; give conditional conclusions and validation levels when useful.

If supporting skills materially affect the conclusion, end with a compact `融合口径` line, for example:

```text
融合口径：moomoo news/digest + moomoo option/capital/technical anomaly + us-stock-gamma-moomoo gamma + stock-technical-analysis price action + macro-news-check tape.
```
