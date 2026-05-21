# Japan Close Briefing

Use for `日股收盘复盘`, `今天日股复盘`, or Japanese market close-review requests.

## Live Sources

Prefer Japanese-language sources:

- kabutan.jp
- finance.yahoo.co.jp
- JPX market data/pages
- トレーダーズ・ウェブ
- みんかぶ
- Nikkei/Reuters/Bloomberg/CNBC Japan when available
- daytrading.monster/pts for after-close PTS movers

## Required Data

- Confirm current date in Japan time and whether the Tokyo market traded today. If closed, state the closure reason and summarize only valid futures/global/after-hours linkage.
- Nikkei 225, TOPIX, Mothers/Growth or relevant small-cap index: close levels and percentage moves.
- USD/JPY, JGB yield, US futures, China/Hong Kong linkage, and major commodity/rate context when relevant.
- Main sector performance and breadth where available.
- Active themes from the fixed focus list and shared theme list, mapped to Japanese stocks.
- Unusual movers with codes or Japanese short names, direction, and catalyst/negative driver.
- Earnings, guidance revisions, buybacks, capital policy, rating changes, policy news, geopolitical events, and after-close PTS moves.
- Apply the shared `Theme Catalyst Discipline` and `Local Market Data Discipline`; close-review reports must scan after-close and next-session catalysts, not only index closes.

## Output Format

First line: 60-80 Chinese-character title starting with `总结今日日股`, containing index direction, core themes, risk signal, and operation guidance.

Then exactly:

一、今日日股市场概述
- 日经225、TOPIX等主要指数收盘数据。
- 大盘强弱、市场宽度、日元/利率/美股或亚洲市场联动。
- 核心涨跌原因，结合最新新闻解释。

二、重点题材与异动个股
- 按题材分类说明：固定关注板块 + 共享固定主题 + 突发题材。
- 重要题材尽量具体到个股代码或日文简称。
- 说明上涨/下跌原因：财报、订单、政策、产业链、资金情绪、PTS、信用/空卖或机构线索。

三、盘后PTS与明日前风险
- PTS急涨/急跌个股及原因。
- 明日前需要关注的美股、汇率、利率、财报、政策、地缘和日股公告风险。
- 判断今日趋势是否可能延续，或是否出现冲高回落/反转信号。

四、对下一交易日的操作指导
- 明确判断下一交易日偏强、偏弱、震荡，或高开低走/低开高走概率。
- 给出题材优先级。
- 给出可执行建议：追高、等回踩、减仓、观察、分批低吸、避开财报风险等。
- 区分短线情绪交易和中长线可持续主线。

## Constraints

- Focus on what today's close means for the next Japan trading session.
- Include specific Japanese tickers or short names for actionable movers.
- Keep the report concise and decision-oriented.
