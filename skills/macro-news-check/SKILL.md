---
name: macro-news-check
description: Use when stock, index, gamma, or market analysis needs current macro or broad-market context from live news sources such as Jin10, Wallstreetcn, and FinancialJuice, especially for rates, FX, central banks, commodities, geopolitics, index moves, market-wide risk sentiment, or sudden cross-asset news.
---

# Macro News Check

Use this skill only when the analysis genuinely needs current macro, broad-market, or cross-asset context. Do not run it for every single-stock question by default.

This skill is public-safe: it uses public pages or feeds and must not store credentials, cookies, account data, private research paths, or raw copyrighted news dumps. Summarize only the headlines and implications needed for the user's market question.

## Trigger Conditions

Call this skill when one or more of these are true:

- The user asks about 大盘, 宏观, 利率, 汇率, 美债, 日债, 央行, CPI/PCE/FOMC/BOJ/ECB, commodities, oil, gold, geopolitics, or market-wide risk sentiment.
- A stock/index/ETF is moving with no clear stock-specific catalyst, or the move may be driven by rates, FX, futures, sector-wide risk, policy, or global headlines.
- Technical analysis needs a broad-market confirmation, especially for index breaks, high-beta stocks, export-sensitive Japanese names, A-share market emotion, US premarket moves, or same-day trading judgments.
- Gamma analysis would be unreliable without checking macro headlines, event risk, vol shock, index futures, yields, USD, or geopolitical tape risk.
- A prior single-stock read may be missing a market-wide reason for a selloff or squeeze.

Do not call this skill when the request is clearly only about static fundamentals, historical valuation, company filings, or a chart level that does not depend on current market tone.

## Source Order

Prefer sources in this order, adjusting for language and market:

1. `Jin10` (`https://www.jin10.com/`): preferred Chinese macro tape when accessible. Its data quality is generally strong for real-time Chinese-language macro, central-bank, commodity, FX, and geopolitical headlines. The homepage can expose server-rendered flash items; the underlying flash API or WebSocket may require frontend headers/cookies and can be more fragile.
2. `Wallstreetcn` (`https://wallstreetcn.com/live/global`): useful Chinese backup and Asia/China market tape. If the page is a frontend shell, try its live JSON endpoint pattern:
   `https://api-one-wscn.awtmt.com/apiv1/content/lives?channel=global-channel&client=pc&limit=10`
3. `FinancialJuice` (`https://www.financialjuice.com/`): useful English global tape, especially US/EU macro, rates, FX, commodities, geopolitics, and market-moving headlines. Public RSS pattern:
   `https://www.financialjuice.com/feed.ashx?xy=rss`

Use more than one source when the headline is important, surprising, or likely to change the market read. Prefer original official sources when a live headline points to a specific data release, central-bank statement, government notice, or company disclosure.

## Workflow

1. Define the macro question before fetching:
   - Is the issue rates, FX, index futures, commodities, geopolitics, policy, or broad risk appetite?
   - Which market matters most: China/A-shares, Japan, US, Europe, global commodities, or cross-asset?
2. Fetch the minimum needed recent items:
   - Start with Jin10 for Chinese macro tape if accessible.
   - Use Wallstreetcn's live endpoint for Chinese/Asia backup and market breadth context.
   - Use FinancialJuice RSS for English global confirmation and US/EU tape.
3. Filter aggressively:
   - Keep only headlines that can plausibly affect the instrument being analyzed.
   - Prioritize timestamps, source type, affected asset class, and whether the item is data, policy, rumor, geopolitical, or routine noise.
4. Classify the macro effect:
   - `risk-on`: supports equities/high beta/cyclical trades.
   - `risk-off`: pressures equities/high beta; supports bonds, USD, defensive assets, or safe havens depending on context.
   - `rates-up pressure`: bad for long-duration growth, high valuation, weak balance sheets, bond proxies.
   - `rates-down support`: can help duration/growth, but check whether rates are falling from recession fear.
   - `FX-driven`: important for exporters, import-cost names, commodities, and ADR/local-market conversions.
   - `commodity shock`: sector-specific tailwind/headwind.
   - `policy/liquidity`: judge size, timing, credibility, and whether it is already expected.
5. Connect the macro tape to the specific analysis:
   - State whether macro is the main driver, a secondary amplifier, or only background noise.
   - Separate stock-specific catalysts from market-wide pressure.
   - Explain expectation gap: what the market likely expected, what the headline/data changed, and whether it was above, in line with, or below expectations.

## Output Style

Keep the macro section concise unless the user asks for a full macro brief. Use this structure when helpful:

1. `宏观结论`: one sentence on whether the tape is risk-on, risk-off, rates/FX-driven, or neutral.
2. `关键消息`: 2-5 relevant headlines with source and time when available.
3. `对标的影响`: how those headlines affect the stock/index/option map being analyzed.
4. `权重`: main driver / secondary amplifier / background only.
5. `需要确认`: what would require a fresh check, original source, or later market reaction.

Do not paste long article text or bulk live-feed items. Paraphrase and cite only the short headline-level evidence needed for the analysis.
