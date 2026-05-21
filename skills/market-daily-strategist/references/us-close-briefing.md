# US Close Briefing

Use for `美股收盘复盘`, `昨晚美股`, or US close-review requests. When the user asks for a morning-style recap, emphasize the latest US close and recent after-hours/futures developments.

## Live Sources

Prefer Yahoo Finance, Bloomberg, CNBC, MarketWatch, Seeking Alpha, TradingView, and other reliable market/news sources.

## Required Data

- Confirm current date in Japan time and ensure the data is the latest for that date.
- Dow, S&P 500, Nasdaq actual closing levels and percentage moves.
- Major sector performance: tech, semiconductors, AI, software, financials, energy, industrials, consumer, healthcare.
- Unusual movers with tickers/short names, direction, catalyst or negative driver.
- Volume/turnover, unusual volume, retail sentiment, institutional or options clues when available.
- Important news/earnings/ratings/policy/geopolitical events from the past 8 hours.
- After-hours futures: Nasdaq futures, S&P 500 futures, Dow futures latest levels and changes.
- Apply the shared `Theme Catalyst Discipline` and `Local Market Data Discipline`; close-review reports must still scan active themes and after-hours catalysts, not only index closes.

If the US market was closed for a holiday, explain the reason and summarize only valid after-hours, futures, and global linkage information.

Do not search or cite `NaNa说美股` unless the user separately asks.

## Output Format

First line: 60-80 Chinese-character title starting with `总结昨晚美股`.

Then exactly:

一、昨晚美股市场概述
- 三大指数真实收盘数据。
- 主要板块表现。
- 核心涨跌原因，结合最新新闻解释。

二、重点题材与异动个股
- 按题材分类说明：固定关注板块 + 共享固定主题 + 突发题材。
- 每个重要题材尽量具体到相关个股或代码。
- 说明上涨/下跌原因：政策预期、财报、订单、供需、产业链、资金情绪、期权/散户情绪等。

三、盘后期货与今日开盘前风险
- 纳指期货、标普期货、道指期货最新变化。
- 是否延续昨晚趋势，是否出现反转信号。
- 地缘、政策、宏观数据、财报、讲话等即将引爆市场的事件。

四、对今天操作的指导意见
- 明确判断今天偏强、偏弱、震荡，或高开低走/低开高走概率。
- 给出板块优先级。
- 给出可执行建议：追高、等回踩、减仓、观察、分批低吸、避开财报风险等。
- 区分短线情绪交易和中长线可持续主线。

## Constraints

- The report is not only a recap; it must lead to today's trading decisions.
- All US market numbers must be sourced live. Do not fabricate.
