# Shared Rules

## Output Language

- Use pure simplified Chinese unless the user explicitly asks otherwise.
- Keep the language professional, objective, concise, and trading-decision oriented.

## Data Discipline

- All market figures must come from live tools or reliable sources: prices, index levels, futures, percentage moves, volume, turnover, flows, gamma/options levels, valuation, financials, ratings, policy/news details, PTS data, and after-hours moves.
- Never fabricate missing data. If unavailable or delayed, write `暂无具体数值`, `初步`, or `数据延迟`.
- Attribute key numbers and important news to sources.
- If using social media, label it as social-media sentiment, not verified fact.
- If using the optional narrative-status helper, treat it as a social-media-derived theme pre-screen. Account/source quality can be assumed acceptable for screening, but timeliness must still be checked: feed `generatedAt`/`reviewedAt` and entry `sourceCreatedAt`/`updatedAt` must fit the report window. Fresh entries can suggest which themes to verify; stale entries are background only and must not drive current-session strategy.
- When internal/current-page helper data is used, do not name DayTrading.monster, 24H Feed, dashboard/widget names, page names, or other aggregator/source names in final report prose by default. Describe the layer generically as `当前叙事预筛`, `当前价格代理`, `PTS异动`, `评级线索`, or `行情确认`. URLs may appear in a dedicated source list when the user asks for sources or when an audit trail is required.

## Market News Discipline

For every pre-market and close-review report, read enough current market news before finalizing. Do not rely only on index futures, macro headlines, earnings calendars, closing index moves, or a few mega-cap tickers.

- Start from broad same-day market-news sources: live flash headlines/快讯, market live blogs, wire recaps, pre-market/after-hours mover summaries, and individual-stock news.
- For U.S. and Japan market analysis, treat the current DayTrading.monster 24H Feed as the most important public theme-discovery source. Use the Market narrative monitor for condensed cross-topic state and the X account monitor for raw account-level market posts before deciding which themes, sectors, or movers deserve deeper verification.
- For broad theme discovery, the optional narrative-status helper can be used before or alongside live news scanning to surface current narratives across AI, geopolitics, commodities, rates/bonds, index/gamma, Japan, China, non-AI sectors, and crypto. It reads the current Market narrative monitor and does not replace the same-day news scan or price/sector confirmation.
- For pre-market and close-review reports, also consider the current DayTrading.monster 24H Feed (`https://daytrading.monster/tools/24hfeed/`) as a social-media-derived source layer with two distinct monitors:
  - `Market narrative monitor`: `https://daytrading.monster/tools/24hfeed/narrative_status.json` gives current topic summaries, timestamps, source timestamps, and X evidence links.
  - `X account monitor`: `https://daytrading.monster/tools/24hfeed/accounts.json` lists monitored accounts and freshness; per-account current market posts are available under paths such as `https://daytrading.monster/tools/24hfeed/{handle}/market_recent.json`, with broader retained posts in `{handle}/market_tweets.json`.
  Do not fetch or mine historical/archive 24H Feed data for normal reports. Do not use the HTML page's `noscript` or static SEO summary as current evidence because it can lag the runtime app. Treat both monitors as social-media-derived screening and verify decisive items with live news, original/source reporting when available, and prices.
- DayTrading.monster home (`https://daytrading.monster/`) can help identify global index, FX, commodity, yield, ETF, and tokenized/proxy TradingView symbols plus `D`, `24h`, and `365d` badges. A plain HTML fetch does not expose the latest widget prices, only the shell, static/noscript news summary, symbols, and badge metadata. Do not cite a live dashboard price or current news read unless it was read from a rendered widget/browser view, a current runtime JSON endpoint, or a programmatic TradingView/scanner equivalent.
- Japan PTS reports must use the current runtime app data (`https://daytrading.monster/pts/data.json`) or a rendered page view, not the static `noscript` SEO fallback. Use `mode1` for day-session movers, `mode2` for after-close movers, and `mode3` for night-session movers; check the matching `mode*UpdatedAt` timestamp before citing a mover.
- In final report prose, do not use site-specific "source shows" phrasing by default. Use neutral descriptions such as `当前叙事预筛`, `当前评级数据有更新`, or `PTS异动名单`. If the rating layer has no relevant current update, omit it instead of writing negative filler.
- For US pre-market and after-hours sessions, do not try to discover every news-driven mover from scratch. Start with reliable pre-market/after-hours mover summaries, earnings-mover roundups, analyst/rating-mover lists, and market-live summaries, then open individual-stock news only for names that actually move or can change the report conclusion.
- Do not transfer the US extended-hours workflow mechanically to other markets. For Japan, use PTS movers first and then explain them with news. For A-shares, there is no stock night session; use important news and topic pages to understand current market hotspots and possible next-day continuations, not to manufacture a nonexistent after-hours mover list.
- Prioritize news by market impact: index/sector weight, actual price move, volume, breadth, after-hours/pre-market reaction, flows, earnings surprise, ratings, policy credibility, and whether the item changes today's trading decision.
- Do not elevate a headline just because it matches a familiar theme or sounds strategically interesting. If the related stocks, ETFs, futures, or sectors are not reacting, treat it as background unless it changes risk.
- If a headline is confirmed but the related price/sector move has not been checked, say so instead of implying a verified trading signal.
- Include only items with actual news, price action, flows, earnings, ratings, policy catalysts, or actionable trading relevance.

## Optional Local / Private Data Discipline

Local/private market-data tools are optional enhancers, not required dependencies. A user who installs this skill may not have moomoo OpenD, MX data/search credentials, private CSV/JSON files, PTS scrapers, or other local scripts configured.

- Do not assume local/private tools are installed, running, permissioned, logged in, or populated. Check availability before relying on them.
- If a local/private tool is unavailable, fails permissions, lacks credentials, or returns stale data, continue with public reliable sources and mark the missing layer as `暂无可靠数值`, `数据不可得`, or `本地工具不可用`.
- Only suggest installing, launching, logging in, or configuring a local/private tool when that layer would materially improve the answer, such as live US gamma, Japan PTS, proprietary watchlists, or account-specific data. Do not make installation a prerequisite for a normal market report.
- Allowed when available: query index ETFs, core sector ETFs, futures/index proxies, gamma/options for relevant US indexes/ETFs, PTS/after-hours pages, and a small number of genuinely important tickers already identified by news, index relevance, or the user's focus.
- For A-share reports and sector/theme questions, 东方财富妙想 skills are optional but preferred when installed. They are supplemental evidence, not a replacement for existing market-news discipline, source hierarchy, price confirmation, emotion-cycle/leader-follower analysis, macro checks, or technical structure. Use `mx-xuangu` for sector/concept constituents, related-stock lists, self-contained condition screens, and peer comparisons; use `mx-data` for A-share quotes, valuation, financials, fund-flow, and board/index data; use `mx-search` for timely news, announcements, policies, research, and event explanations. If unavailable, continue with public reliable sources and optionally suggest installation/configuration only when it would materially improve the exact request.
- Do not touch account-sensitive 妙想 tools unless explicitly requested. Use `mx-zixuan` only for 东方财富 self-selected-stock query/add/delete/filter tasks, and `mx-moni` only for simulated-portfolio or simulated-trading tasks.
- Do not bulk-scan all stocks or all theme constituents for a daily market report unless the user explicitly asks for a broad screener.
- When a data source has explicit extended-hours fields, use only those fields for extended-hours claims. For US pre/post-market moomoo data, use `pre_*`, `after_*`, or `overnight_*` fields as appropriate; do not treat `last_price`, regular-session OHLC, or regular-session volume as pre-market or after-hours data.
- If the correct extended-hours field is unavailable, write `盘前暂无可靠数值`, `盘后暂无可靠数值`, or `数据不可得` instead of substituting stale regular-session data.
- State the field basis correctly when it matters, especially around US pre-market/after-hours, Japan PTS, and futures/index proxies.

## Cross-Skill Use

- Use supporting skills only for points that can change the report conclusion, not for every stock in a mover list.
- Prefer `macro-news-check` for macro/快讯 confirmation before making a rates, oil, FX, geopolitical, or broad-risk claim.
- Prefer `us-stock-gamma-moomoo` for US index gamma/options-wall work when available; if the skill, moomoo OpenD, SDK, quote permission, or live gamma data is unavailable, mark the value unavailable instead of substituting stale public screenshots, and optionally suggest setup only if the user needs that layer.
- Use move-reason skills only for a few decisive movers, such as the day's theme leader, largest liquid abnormal mover, or a stock whose catalyst is unclear but important.
- Use `stock-technical-analysis` for execution levels on selected indexes or key stocks, especially when recommending 追高、等回踩、低吸、减仓、止损.
- Compress supporting-skill findings into the required report structure. Do not append unrelated deep-dive sections unless the user asks.

## Medium/Long-Term Strategy Lens

When the report needs market-regime, mainline, or bull/bear structure judgment, combine current data with the `mainline x funds x game x cycle` framework from `references/global-mainline-funds-game-cycle.md`.

- Treat `mainline` as the durable narrative or industry transition, not one-day theme heat.
- Treat `funds` as the liquidity and positioning condition that determines whether the narrative can keep being priced.
- Treat `game` and `cycle` as the market-structure and timing lenses that decide whether to attack, hold, rotate, defend, or wait.

## Silent Methodology For Long-Term Recommendations

Apply the user's strategy framework silently. Do not expose private source-framework labels or mnemonic names; use plain terms such as 长期均线、趋势支撑、均线密集区、反转结构、突破回踩.

Cover, as relevant:

- beta: market strength/weakness, trend, sector beta, macro/geopolitical risk, volatility.
- trend and support/resistance: moving averages, MA144/long-cycle averages, GMMA, Vegas-style channels, VWAP, Fibonacci, gaps.
- momentum and reversal: RSI, MACD, KDJ, Japanese candlestick continuation/reversal structures, volume-price relationship.
- sentiment and positioning:情绪周期,资金流,期权/gamma, put/call ratio, short interest/空卖, credit margin data when market-specific.
- fundamentals and catalysts: latest earnings, valuation, industry trend, policy/news, orders, buybacks, lock-up expiry, financing/warrants when relevant.
- risk management: entry, batch plan, stop-loss reference, invalidation conditions.
