# A-Share Pre-Market Strategy

Use for `A股盘前策略`, `A股早盘`, or mainland China pre-market strategy requests.

## Live Sources

Prefer 东方财富、同花顺、雪球、财联社、新浪财经 and other reliable Chinese market/news sources.
For topic heat, Eastmoney Guba topics can be used: `https://gubatopic.eastmoney.com/`.

## Required Data

- First confirm whether today is an A-share trading day. If closed, state the closure reason and overnight/global risks; do not output normal trading strategy.
- A-share pre-market futures/index expectations: Shanghai Composite, Shenzhen Component, ChiNext, or overseas mapping when direct pre-market data is unavailable.
- Northbound, main-fund, ETF-fund clues. If no pre-market live data is available, explicitly say unavailable.
- Main sector heat and unusual themes.
- Key unusual stocks and Dragon-Tiger List references, including speculative/institutional movement.
- A-shares have no stock night session. Do not write a nonexistent after-hours mover list; instead use same-day/prior-after-close important stock-site news and Eastmoney Guba topic heat to identify current market hotspots and possible next-day continuations.
- After-close news from the prior day: policy expectations, breaking catalysts, earnings/announcements/regulatory information, and Eastmoney Guba topic heat when relevant.
- Apply the shared `Market News Discipline` and `Optional Local / Private Data Discipline`; A-share pre-market reports must scan active domestic/offshore catalysts, not only index expectations and yesterday's hot sectors.
- When 东方财富妙想 skills are available, use `mx-search` for prior-after-close policy/news/announcements and `mx-data` for A-share index/sector/fund-flow confirmation. Use `mx-xuangu` selectively to identify sector/concept constituents or related stocks for the few themes that can change the morning strategy; do not run a broad all-market screener unless the user asks.

## Output Format

First line: 60-80 Chinese-character long title containing pre-market expectation, core sector trend/reversal signal, and operation signal.

Then exactly:

1. 盘前市场概览
- 期货/外围映射/指数预期。
- 北向资金、主力资金或ETF资金线索。
- 整体开盘氛围和核心驱动因素。

2. 重点板块与异动题材
- 具体板块热度、重点个股代码或简称、趋势/反转信号、催化剂。
- 优先覆盖当天真正有异动、成交确认或交易意义的板块与个股。
- 结合政策预期、业绩线、产业链供需、游资情绪、龙虎榜或机构席位信息。

3. 早盘操作策略
- 开盘预期：偏强、偏弱、震荡、高开低走或低开高走概率。
- 重点关注题材优先级。
- 短线与日内交易机会。
- 关键支撑/阻力、仓位建议、止损参考。
- 明确给出追高、等回踩、低吸、减仓、观察的判断。

## Constraints

- 100% focus on today's morning session.
- Include both market-wide expectation and specific sectors/stocks with trend or reversal signals.
- Keep the conclusion directly usable before the open.
