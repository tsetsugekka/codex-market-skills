# A-Share Long-Term Recommendation

Use for `A股长线推荐`.

## Live Sources

Prioritize 东方财富、同花顺、雪球、财联社、新浪财经 and other reliable Chinese market/news sources.

## Selection Rules

- First verify whether the next mainland China trading session is open. If closed for weekend/holiday, state that briefly and do not force a recommendation.
- Recommend exactly one A-share main-board stock or eligible ETF/LOF.
- Stock recommendations should in principle be A股主板 only; do not recommend 创业板、科创板、新三板 individual stocks.
- 科创板/创业板 related ETF/LOF are allowed, such as 科创50 ETF、创业板ETF.
- Confirm the target can be bought on the next A-share trading day.
- Avoid recently recommended names when the history is available.
- Must show medium/long-term continuity plus confirmed trend or reversal signal and short-term upward momentum.
- Avoid pure left-side bottom fishing or no-momentum targets.
- Buy price must be latest/current price or within 2% of it.

## Required Analysis

Start from beta environment:

- Market strength/weakness, trend, sector strength, geopolitical or macro risk.

Then analyze:

- Technical reversal/trend signals, fundamentals, news/policy catalysts, sentiment recovery, industry outlook, short-term upward momentum, medium/long-term continuity.
- A-share specifics: 大盘指数、板块强弱、两融余额/融资买入、北向/主力资金、ETF资金流、龙虎榜/机构席位、限售解禁、股东减持、政策催化、成交额/换手率、筹码集中度、涨停/炸板/情绪周期.

## Output Format

First line must be 60-80 Chinese characters:

`信心度XX%：A股长线推荐：标的名称（代码，市场类型）——核心逻辑，买入价位X元，目标价位X-X元`

Then exactly:

1. 推荐标的概览（股票/ETF名称、代码、市场类型、当前买入价位）。
2. 推荐核心原因（must start with current beta analysis: market strength/weakness, trend, sector strength, geopolitical or macro risk; then analyze technical reversal/trend signals, fundamentals, news/policy catalysts, sentiment recovery, industry outlook, short-term upward momentum and medium/long-term continuity）。
3. 买入策略（买入价位、suggested batch-buying method, and whether it can be executed immediately on the next trading day）。
4. 目标价位与持有周期（specific target range, expected holding period, and main upside catalysts）。
5. 风险提示（main downside risks and stop-loss reference level）。
6. 信心度：XX%（综合判断本次推荐的确定性）。

End or include clearly: `以上不是投资建议。`
