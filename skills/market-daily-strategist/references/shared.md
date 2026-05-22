# Shared Rules

## Output Language

- Use pure simplified Chinese unless the user explicitly asks otherwise.
- Keep the language professional, objective, concise, and trading-decision oriented.

## Data Discipline

- All market figures must come from live tools or reliable sources: prices, index levels, futures, percentage moves, volume, turnover, flows, gamma/options levels, valuation, financials, ratings, policy/news details, PTS data, and after-hours moves.
- Never fabricate missing data. If unavailable or delayed, write `暂无具体数值`, `初步`, or `数据延迟`.
- Attribute key numbers and important news to sources.
- If using social media, label it as social-media sentiment, not verified fact.

## Market News Discipline

For every pre-market and close-review report, read enough current market news before finalizing. Do not rely only on index futures, macro headlines, earnings calendars, closing index moves, or a few mega-cap tickers.

- Start from broad same-day market-news sources: live flash headlines/快讯, market live blogs, wire recaps, pre-market/after-hours mover summaries, and individual-stock news.
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

## Silent Methodology For Long-Term Recommendations

Apply the user's strategy framework silently. Do not expose private source-framework labels or mnemonic names; use plain terms such as 长期均线、趋势支撑、均线密集区、反转结构、突破回踩.

Cover, as relevant:

- beta: market strength/weakness, trend, sector beta, macro/geopolitical risk, volatility.
- trend and support/resistance: moving averages, MA144/long-cycle averages, GMMA, Vegas-style channels, VWAP, Fibonacci, gaps.
- momentum and reversal: RSI, MACD, KDJ, Japanese candlestick continuation/reversal structures, volume-price relationship.
- sentiment and positioning:情绪周期,资金流,期权/gamma, put/call ratio, short interest/空卖, credit margin data when market-specific.
- fundamentals and catalysts: latest earnings, valuation, industry trend, policy/news, orders, buybacks, lock-up expiry, financing/warrants when relevant.
- risk management: entry, batch plan, stop-loss reference, invalidation conditions.
