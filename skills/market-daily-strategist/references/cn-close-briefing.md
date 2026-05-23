# A-Share Close Briefing

Use for `A股收盘复盘`, `今天A股复盘`, or mainland China market close-review requests.

## Live Sources

Prefer 东方财富、同花顺、财联社、雪球、新浪财经、证券时报、上海证券报 and other reliable Chinese market/news sources. For topic heat, Eastmoney Guba topics can be used: `https://gubatopic.eastmoney.com/`.

## Required Data

- Confirm current date in Japan time and whether A-shares traded today. If closed, state the closure reason and summarize only relevant offshore/global/futures/news linkage.
- Shanghai Composite, Shenzhen Component, ChiNext, STAR 50 or CSI 300 where relevant: close levels and percentage moves.
- Turnover, market breadth,涨跌家数, limit-up/limit-down,炸板率, emotion-cycle clues when available.
- Northbound/main-fund/ETF-fund clues; if unavailable, say so.
- Main sector and theme performance, mapped to A-share concepts and tradable names.
- Unusual stocks with codes/short names, direction, catalyst/negative driver, and Dragon-Tiger List/机构席位 clues when available.
- A-shares have no stock night session. Do not write a nonexistent after-hours mover list; use after-close policy/news/announcements/earnings/regulatory information and Eastmoney Guba topic heat to identify current market hotspots and possible next-day continuations.
- Apply the shared `Market News Discipline` and `Optional Local / Private Data Discipline`; close-review reports must scan after-close and next-session catalysts, not only index closes and today's hot sectors.
- When 东方财富妙想 skills are available, use `mx-data` for index, sector, breadth/fund-flow, valuation, and key-stock quote confirmation; use `mx-search` for after-close news, announcements, policy, research, and event explanations; use `mx-xuangu` to map sector/concept constituents or related stocks for important themes. If unavailable, continue with public sources and state uncertainty where needed.

## Output Format

First line: 60-80 Chinese-character title starting with `总结今日A股`, containing index direction, core themes, sentiment signal, and next-session operation guidance.

Then exactly:

一、今日A股市场概述
- 上证、深证、创业板等主要指数收盘数据。
- 成交额、市场宽度、涨停/跌停、情绪周期和资金面线索。
- 核心涨跌原因，结合政策、外围、行业和资金变化解释。

二、重点板块与异动个股
- 按市场影响排序说明真正活跃的板块、题材和异动个股。
- 重要题材必须尽量具体到A股代码或简称。
- 说明上涨/下跌原因：政策预期、业绩线、产业链供需、游资情绪、龙虎榜、机构席位、ETF资金等。

三、盘后消息与下一交易日风险
- 盘后重要公告、政策、监管、财报、减持/解禁、龙虎榜或资金变化。
- 外围市场、港股/中概、汇率、商品和地缘事件风险。
- 判断今日主线是否可能延续，或是否存在高位分歧/退潮风险。

四、对下一交易日的操作指导
- 明确判断下一交易日偏强、偏弱、震荡，或高开低走/低开高走概率。
- 给出题材优先级。
- 给出可执行建议：追高、等回踩、减仓、观察、分批低吸、避开公告/监管风险等。
- 区分短线情绪交易和中长线可持续主线。

## Constraints

- Do not only recap; translate today's close into next-session strategy.
- Include concrete sectors and stock codes where actionable.
- Keep the tone professional, concise, and risk-aware.
