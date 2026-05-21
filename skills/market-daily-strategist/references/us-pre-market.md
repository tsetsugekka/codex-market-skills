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
- Main pre-market sector performance: AI semiconductors, memory, tech, software, consumer, financials, new energy, energy, defense, and other active focus themes.
- Pre-market movers with ticker/short name, move direction, and catalyst or negative driver.
- Latest major news: earnings, policy, geopolitical events, Trump-related news, oil, Treasury yields, inflation expectations, economic data, speeches.

## Theme Catalyst Scan

Before finalizing the report, run a targeted headline scan for active themes. Do not rely only on index futures, macro headlines, earnings calendars, or a few mega-cap tickers.

- Search current pre-market/news wires for the user's fixed themes and any obvious active tape themes, especially: AI chips/accelerators, model/cloud partnerships, quantum computing, robotics/humanoids, autonomous driving/FSD, EVs, commercial space, defense, data centers/NeoCloud, energy/oil, crypto/stablecoins, memory, software/SaaS, and consumer.
- Include a theme only when there is a same-day or clearly current catalyst, pre-market move, policy item, earnings/guidance item, rating action, funding/subsidy news, or credible market-wide flow.
- Examples of catalysts that must not be missed when current: Tesla FSD/China approval or rollout news; US quantum-computing funding and related pre-market moves; Anthropic/Claude cloud, chip, or Microsoft/NVIDIA partnership headlines; SpaceX launch/IPO/contract news; AI system shipment updates such as NVIDIA Vera Rubin.
- If a theme headline is confirmed but the related stock price is not checked, say so instead of implying a verified move.
- If a theme is active outside the fixed focus list, label it `新增/突发题材`.

## Moomoo / Local Data Discipline

Use moomoo or local market-data skills selectively. They are for confirmation, not broad discovery.

- Allowed: query US index ETFs, core sector ETFs, SPX/SPY/QQQ gamma, and a small number of genuinely important tickers already identified by news or index relevance.
- Do not use moomoo or local skills to bulk-scan all US stocks or all theme constituents for a pre-market report.
- During US pre-market, use only explicit extended-hours fields such as `pre_price`, `pre_change_rate`, `pre_volume`, `pre_high_price`, and `pre_low_price` as pre-market data.
- Do not treat `last_price`, `open_price`, `high_price`, `low_price`, `volume`, or regular-session OHLC fields as pre-market values. If `pre_*` fields are unavailable, write `盘前暂无可靠数值`.
- When using ETF/stock pre-market quotes, state or imply the field basis correctly; do not mix prior regular-session `last_price` with current pre-market `pre_price`.

## Output Format

First line: 60-80 Chinese-character long title containing futures, key derivative indicator such as Gamma/options wall/CTA, core themes, and trading signal.

Then exactly:

1. 盘前期货与衍生品概览
- 三大期货最新变化。
- SPX Gamma、Gamma Flip、Gamma Wall、JPM期权墙、CTA flow。
- 解释这些关键位置对开盘和日内走势的影响。

2. 主要板块与异动个股
- 具体板块盘前表现、重点ticker、催化或利空。
- 覆盖当天真正有异动或交易意义的固定关注板块；不要打开或依赖 DTM `/themes` 项目，除非用户明确要求。
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
- Do not skip the theme catalyst scan just because index futures and macro data are available.
