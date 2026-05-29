# US Stock Move Reason

`us-stock-move-reason` 是一个美股异动原因分析 skill，用来把官方 moomoo 新闻、社区、资金异动、期权异动、技术异动，以及本仓库已有的 gamma、技术、情绪和宏观 skill 汇总成一份证据驱动的中文结论。

## 能做什么

- 分析美股或 ETF 为什么急涨、急跌、盘前跳空、盘后异动。
- 用 `moomoo-news-search` / `moomoo-stock-digest` 抓取和解释公司新闻、财报、指引、评级、订单、监管和行业 read-through。
- 用 `moomoo-comment-sentiment` 读取 moomoo 社区讨论温度和代表性观点。
- 用 `moomoo-capital-anomaly` 检查资金、短卖、资金流向等异动。
- 用 `moomoo-derivatives-anomaly` 检查美股适用的期权大单、IV、量价、期权情绪和综合信号；不调用港股牛熊证维度。
- 用 `moomoo-technical-anomaly` 做官方技术异动扫描，再由 `stock-technical-analysis` 验证趋势、VWAP、均线、量价、动能背离和支撑压力。
- 对期权活跃股或指数/ETF，调用 `us-stock-gamma-moomoo` 读取 gamma/GEX、gamma wall、flip 和 0DTE 结构。
- 当 Fed、利率、美元、油金、指数期货或地缘风险可能影响解释时，调用 `macro-news-check`。

## 典型请求

```text
DELL 为什么暴涨？
```

```text
NVDA 盘后为什么跌，moomoo 评论和期权大单怎么看？
```

```text
SPY 今天是宏观原因还是技术突破？
```

## 【依赖】

- 可选但推荐：官方 moomoo skills，包括 `moomoo-news-search`、`moomoo-stock-digest`、`moomoo-comment-sentiment`、`moomoo-capital-anomaly`、`moomoo-derivatives-anomaly`、`moomoo-technical-anomaly`。
- 可选但推荐：本机 moomoo OpenD 和 Python SDK，用于行情、K线、期权、资金和技术异动数据。
- 可选协同：`us-stock-gamma-moomoo`、`stock-technical-analysis`、`stock-sentiment-analysis`、`macro-news-check`。

## 【协同调用】

- `us-stock-gamma-moomoo`：期权/gamma/0DTE/SPX/SPY/QQQ 结构。
- `stock-technical-analysis`：技术结构、支撑压力、VWAP、分时确认。
- `stock-sentiment-analysis`：情绪周期、拥挤交易、期待差和社区热度。
- `macro-news-check`：Fed、利率、美元、商品、指数期货和地缘风险。

## 输出结构

固定输出：

1. `最有力理由`
2. `补助理由`
3. `期权/资金/技术异动`
4. `社区情绪`
5. `确定度`
6. `注意点`

## 公开安全说明

这个 skill 只保存公开安全的工作流说明，不保存 moomoo 账号、OpenD 日志、API key、cookie、个人持仓、截图、私有 RAG 或原始研究资料。输出仅用于研究，不构成投资建议。
