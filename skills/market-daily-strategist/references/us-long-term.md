# US Long-Term Recommendation

Use for `美股长线推荐`.

## Live Sources

Prioritize Yahoo Finance, Seeking Alpha, Bloomberg, TradingView, CNBC, MarketWatch. Avoid low-quality blogs. Social media can be used only as labeled sentiment.

## Selection Rules

- Recommend exactly one US stock.
- Avoid recently recommended names when the history is available.
- The stock must have medium/long-term continuity plus confirmed trend or reversal signal and near-term upward momentum.
- The buy price must be latest available/current price or within 2% of it.
- If the regular US session has not opened, clearly say the price is pre-market or latest available, not regular-session live price.

## Required Analysis

Start from beta environment:

- Major index strength/weakness, trend, sector strength, geopolitical risk, volatility, options/gamma environment.

Then analyze:

- Technical trend/reversal signal, support/resistance, volume-price relationship, moving averages, MA144, Vegas-style channels, MACD, KDJ, RSI, GMMA, VWAP, Fibonacci, gaps, Japanese candlestick patterns, Wyckoff structure, sentiment cycle.
- Fundamentals, industry cycle, news/policy catalyst, institutional holding, short interest, options put/call ratio, gamma wall, buybacks, lock-up expiry.

## Output Format

First line: 60-80 Chinese-character title:

`信心度XX%：美股长线推荐……`

The title must include stock name/code, core logic, buy price, and target price.

Then exactly:

1. 推荐股票概览（股票名称、代码、当前买入价位）。
2. 推荐核心原因（先分析 beta 环境，再拆解短期向上动能与中长线持续性）。
3. 买入策略（买入价位、分批方式、当天是否可立即执行）。
4. 目标价位与持有周期（具体目标价位区间、预期持有周期、主要上行催化剂）。
5. 风险提示（主要下行风险及止损参考位）。
6. 信心度：XX%（综合确定性）。

End or include clearly: `以上不是投资建议。`
