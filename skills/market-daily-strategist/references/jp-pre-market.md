# Japan Pre-Market Strategy

Use for `日股盘前策略`, `日经盘前`, or Japan pre-market strategy requests.

## Live Sources

Prefer Japanese-language sources and keywords:

- kabutan.jp
- finance.yahoo.co.jp
- daytrading.monster/pts
- トレーダーズ・ウェブ
- みんかぶ
- `日経先物最新`
- `PTS急騰銘柄`
- `本日の注目セクター`

## Required Data

- First confirm whether today is a Japan market trading day. If closed, state the closure and briefly note overnight risks; do not output normal trade advice.
- Nikkei 225 futures latest level and expected move.
- PTS sharp risers/fallers, prioritizing `https://daytrading.monster/pts/`.
- Main pre-market theme heat, unusual stocks, speculative/institutional flow references.
- Important after-close news, policy expectations, breaking news, earnings, and rating changes.
- Apply the shared `Market News Discipline` and `Optional Local / Private Data Discipline`; Japan pre-market reports must scan active global/Japan news and catalysts, not only Nikkei futures and PTS movers.

## Output Format

First line: 60-80 Chinese-character title containing probability/strength judgment, futures expectation, today's core themes, and operation signal.

Then exactly:

1. 今天日股盘前概述
- 期货最新点位、整体预期、核心驱动因素。
- 结合昨晚美股、日元、利率、商品、政策和昨天盘后新闻解释。

2. 重点题材与异动个股
- 具体板块、个股代码或日文简称、潜在题材、游资情绪、政策催化。
- 优先覆盖当天真正有异动、成交确认或交易意义的板块与个股。

3. 操作指导
- 短线日内机会。
- 筑底期长线左侧/右侧布局建议。
- 仓位建议、买入节奏、追高/低吸/观望/减仓判断。
- 关键风险点。

4. 风险提示与保本铁律
- 始终强调保存实力。
- 明确说明哪些情况应降低仓位或停止追高。

## Constraints

- 100% front-looking for today. Do not dump yesterday's closing data.
- Include specific stock codes or Japanese short names for actionable names.
- Blend speculative sentiment, policy expectations, fundamentals, and technicals.
