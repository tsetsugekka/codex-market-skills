# Stock Technical Analysis

`stock-technical-analysis` 是一个用于 Codex 的股票技术分析 skill。它面向美股、日股和 A 股，聚焦技术结构、分时走势、支撑压力、均线、量价、KDJ/MACD/RSI、Vegas 通道，以及“能不能到某个价位”的盘中判断。公开版是自包含版本，不依赖私有 RAG 或私有资料。

## 能做什么

- 判断个股当前是强趋势延续、空中加油候选、回踩确认、冲高回落、高位分歧或破位反抽。
- 分析支撑位、压力位、突破/回踩是否确认，以及 touch、break、tradable hold 的区别。
- 结合成交量、KDJ、MACD、RSI、VWAP、短期均线和 Vegas EMA 通道判断动能。
- 读取 moomoo、Yahoo Finance、券商图表或截图时，按多周期图表流程给出当前读数、结构、量价/动能、执行含义和下一验证点。
- 对美股个股，可先用 `moomoo-technical-anomaly` 做官方技术异动扫描；但该结果只是提示，最终仍按趋势位置、VWAP/均线、量价、动能背离、支撑压力和失败突破判断。
- 与日股、A 股、美股 gamma 等市场 skill 配合：先找催化/基本面，再看技术结构是否确认。

## 【依赖】

- 可选：`mx-data`、`mx-search`、`mx-xuangu`，用于 A 股行情、资讯、板块/概念成分、同行对比和自然语言技术筛选增强。
- 可选：`mx-zixuan`，仅在用户明确要求东方财富自选股任务时使用。
- 可选：`moomoo-technical-anomaly`，用于美股官方技术异动扫描。

## 【协同调用】

- `macro-news-check`、`stock-sentiment-analysis`、`cn-stock-move-reason`、`jp-stock-move-reason`、`us-stock-move-reason`、`us-stock-gamma-moomoo`。

## 典型请求

```text
现在这个股票技术面怎么看，压力位和支撑位在哪里？
```

```text
它今天能不能冲到 240？
```

```text
这算突破确认还是冲高回落？
```

```text
结合 moomoo 图表，看一下是不是空中加油。
```

## 公开安全说明

这个 skill 只保存通用技术分析规则，可以放在公开仓库中。请不要提交个人仓位、交易计划、私有研究路径、截图原图、专有指标名、私有人名/handle、私有策略标签、`.env`、token 或任何含登录信息的文件。默认分析不读取私有 RAG；除非用户明确指定某个文件，否则只使用 skill 自带参考、当前图表/截图和行情上下文。

如果用户希望结合自己的学习资料，应引导用户在公开仓库外建立私有 RAG/知识库，并可帮助建立本地索引。原始 PDF、截图、指标和笔记留在私有库中；只有抽象后的通用经验可以在用户明确要求时写入 skill。允许保留 Vegas、KDJ、MACD、RSI、VWAP、支撑压力等通用概念；不要写入原创策略名、私有人名/handle、私有文档名或独特标签。

本 skill 输出仅用于个人研究，不构成投资建议。技术分析只描述条件和概率，不应被当成确定性交易指令。
