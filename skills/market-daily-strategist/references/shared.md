# Shared Rules

## Output Language

- Use pure simplified Chinese unless the user explicitly asks otherwise.
- Keep the language professional, objective, concise, and trading-decision oriented.

## Data Discipline

- All market figures must come from live tools or reliable sources: prices, index levels, futures, percentage moves, volume, turnover, flows, gamma/options levels, valuation, financials, ratings, policy/news details, PTS data, and after-hours moves.
- Never fabricate missing data. If unavailable or delayed, write `暂无具体数值`, `初步`, or `数据延迟`.
- Attribute key numbers and important news to sources.
- If using social media, label it as social-media sentiment, not verified fact.

## News Coverage Discipline

For every pre-market and close-review report, read enough current market news before finalizing. Do not rely only on index futures, macro headlines, earnings calendars, closing index moves, or a few mega-cap tickers.

- Start from broad same-day market-news sources: live flash headlines/快讯, market live blogs, wire recaps, pre-market/after-hours mover summaries, and individual-stock news. Then infer active themes from the news flow.
- After reading the broad news flow, map only the relevant items to the fixed focus themes below or to `新增/突发题材`.
- Treat the fixed focus themes as a classification and priority lens, not as a checklist to search one by one. In routine daily reports, it is usually better to read pre-market/after-hours news flashes and third-party market summaries first, then map any discovered catalysts back to the user's focus themes.
- Include only themes with actual news, price action, flows, earnings, ratings, policy catalysts, or actionable trading relevance. Do not mechanically search or comment on every fixed theme.
- If a theme headline is confirmed but the related stock/sector move is not checked, say so instead of implying a verified move.
- Mark active themes outside the fixed list as `新增/突发题材`.
- Use past misses only as calibration examples, not as a fixed checklist. For example, on 2026-05-21 the report initially missed Tesla FSD/China rollout news, US quantum-computing funding, and AI-infrastructure partnership/chip-roadmap headlines because the news scan was too narrow. The durable rule is to read broader current market news before deciding what the active themes are, not to search those exact themes every day.

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

## Fixed Focus Themes

Long-term user focus themes:

半导体、电网/特高压、新能源、商业航天、AI应用、存储芯片、光伏、储能、光纤、军工、电池、造船、机器人、消费。

Fixed shared Chinese theme list:

数据中心/NeoCloud、具身智能/机器人、商业航天/航天、稀土、无人机/低空经济、军工/防务、功率半导体、模拟半导体、存储芯片、半导体代工、MLCC、PCB、量子计算、钙钛矿太阳能电池、全固态电池、蓄电池、光器件/光模块、石油/天然气、半导体材料/零部件、地方银行、综合商社、大型银行/互联网银行、造船、核聚变发电、日元贬值受益、日元升值受益、网络安全、软件/SaaS、互联网服务、电力/燃气、建筑公司/建设工程、电气设备、加密货币、稳定币、光纤、CPU/GPU/TPU、娱乐/游戏、零售、餐饮、玻璃纤维布/铜箔、人造金刚石、减肥药/肥胖症治疗药、创新药/新药、汽车/汽车零部件、电动汽车、自动驾驶、铁路、航空/邮轮/旅游、农业、猪肉、黄金/白银、铜/铜冶炼、稀有金属、其他金属、海运、消费金融、保险、证券、房地产、可再生能源、化工、物流、煤炭、半导体制造/测试设备、水务基础设施、变压器/HVDC、数据中心冷却系统、工程机械。

Usage:

- Do not open or depend on the DTM `/themes` project or `https://daytrading.monster/themes/` unless the user explicitly asks to update or inspect that project.
- Deduplicate, merge, and map the fixed themes to the relevant market's tradable sectors, stocks, ETFs, or concepts.
- Do not mechanically comment on every item. Only analyze active themes with real movement, news, flow, policy, earnings, ratings, or trading relevance.
- Mark active themes outside the fixed list as `新增/突发题材`.

## Silent Methodology For Long-Term Recommendations

Apply the user's strategy framework silently. Do not expose private source-framework labels or mnemonic names; use plain terms such as 长期均线、趋势支撑、均线密集区、反转结构、突破回踩.

Cover, as relevant:

- beta: market strength/weakness, trend, sector beta, macro/geopolitical risk, volatility.
- trend and support/resistance: moving averages, MA144/long-cycle averages, GMMA, Vegas-style channels, VWAP, Fibonacci, gaps.
- momentum and reversal: RSI, MACD, KDJ, Japanese candlestick continuation/reversal structures, volume-price relationship.
- sentiment and positioning:情绪周期,资金流,期权/gamma, put/call ratio, short interest/空卖, credit margin data when market-specific.
- fundamentals and catalysts: latest earnings, valuation, industry trend, policy/news, orders, buybacks, lock-up expiry, financing/warrants when relevant.
- risk management: entry, batch plan, stop-loss reference, invalidation conditions.
