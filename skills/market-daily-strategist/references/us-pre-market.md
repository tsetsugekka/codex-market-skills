# US Pre-Market Strategy

Use for `美股盘前策略`, `美股开盘前`, or US pre-market strategy requests.

## Live Sources

Prefer Yahoo Finance, Bloomberg, CNBC, MarketWatch, Seeking Alpha, TradingView. Search as needed for:

- `美股盘前期货`
- `SPX gamma exposure`
- `SPX gamma flip gamma wall`
- `JPMorgan options wall`
- `CTA flow`

## Required Data

- Nasdaq futures, S&P 500 futures, Dow futures: latest level and change.
- SPX Gamma Exposure: gamma level, Gamma Flip, Gamma Wall.
- JPMorgan options wall or key options-wall levels.
- CTA flow latest dynamic.
- Main pre-market sector performance and active themes, ranked by actual futures/ETF/stock reaction and trading relevance.
- Pre-market movers with ticker/short name, move direction, and catalyst or negative driver.
- Latest major news: earnings, policy, geopolitical events, Trump-related news, oil, Treasury yields, inflation expectations, economic data, speeches.
- Apply the shared `Market News Discipline` and `Optional Local / Private Data Discipline`; do not skip broad market-news scanning just because futures, macro data, or mega-cap earnings are available.

## Output Format

First line: 60-80 Chinese-character long title containing futures, key derivative indicator such as Gamma/options wall/CTA, core themes, and trading signal.

Then exactly:

1. 盘前期货与衍生品概览
- 三大期货最新变化。
- SPX Gamma、Gamma Flip、Gamma Wall、JPM期权墙、CTA flow。
- 解释这些关键位置对开盘和日内走势的影响。

2. 主要板块与异动个股
- 具体板块盘前表现、重点ticker、催化或利空。
- 优先覆盖当天真正有异动、成交确认或交易意义的板块与个股。
- 结合财报、评级、政策、供需、资金情绪、期权/游资情绪解释。

3. 今天开盘前瞻与操作策略
- 总体开盘预期：偏强、偏弱、震荡、高开低走或低开高走概率。
- 核心题材优先级。
- 短线与日内机会。
- 关键支撑/阻力、仓位建议、止损参考。
- 明确给出追高、等回踩、低吸、减仓、观察的判断。

## Constraints

- Focus 100% on today's pre-market. Do not recap yesterday's close except where needed as context.
- Use specific tickers for actionable movers.
- Keep the report concise and strategy-oriented.
