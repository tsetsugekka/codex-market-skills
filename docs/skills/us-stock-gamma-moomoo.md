# US Stock Gamma Moomoo

`us-stock-gamma-moomoo` 是一个用于 Codex 的美股期权 gamma 分析 skill。它通过本机 moomoo OpenD 获取美股和期权数据，再由 Codex 输出 gamma/GEX、gamma wall、gamma flip、SPX/SPY/ES 盘中结构和 0DTE 期权情景表。公开版是自包含版本，不依赖本地 `Stocks` 文件夹或私有资料。

## 能做什么

- 分析普通美股或美股 ETF 的期权 gamma 结构。
- 分析 `.SPX`/SPXW 指数期权结构；SPX/标普500请求优先使用专用 `spx_intraday_latest.py`，用 `US..SPX` 链和 SPXW 0DTE 平价锚，不把普通 SPY/ETF 报告当最终结果。
- 分析日经225时，用 EWJ 期权作为代理 book，再走时间对齐换算：EWJ quote time 的 NKDmain/日经期货锚 -> 当前 NKDmain -> 当前 NIYmain/日经 CFD；不直接展示原始 EWJ strike，也不把已收盘 EWJ 和当前日经 CFD 直接相除。
- 如果拿不到更好的时间对齐锚，使用用户留存兜底公式：`日经目标位 = 62038 × EWJ目标价 / 91.265`，并在结论里标注这是 fallback。
- 指数专用流程默认输出 JSON 和文字总结；HTML 只有用户明确要求时才生成。
- 识别正 gamma wall、负 gamma pit、gamma flip、pin/阻力/支撑区域。
- 对 0DTE call/put 生成“时间 x 标的价位”的理论价值表，用来评估回本、止盈、止损或是否值得继续拿。
- 需要时生成本地 HTML 报告；盘中快问可以只输出文字结论。

## 典型请求

```text
查一下这只美股的 gamma，阻力位和这周可能去的位置。
```

```text
结合 .SPX 期权链、SPY 和 ES，判断 SPX 接下来两小时怎么走。
```

```text
算一下 SPXW 0DTE 7370C 在不同时间和 SPX 点位下的理论价值。
```

## 环境要求

- 需要本机安装并运行 moomoo OpenD。
- 需要 Python SDK `moomoo` 可导入。
- OpenD 需要保持后台运行；行情权限不足时，部分指数或期权数据可能不可用。
- 通用报告脚本会对 `get_option_chain` 主动限速，并在 OpenD 返回“每30秒最多10次”一类错误后等待重试；项目脚本里的同类修复应同步回这个 skill。
- 指数专用算法必须保存在 skill 脚本中：SPX/SPXW 用 `scripts/spx_intraday_latest.py`，日经/EWJ 转 NKDmain/NIYmain/CFD 用 `scripts/proxy_index_gamma.py`。
- 这个 skill 只需要行情和期权链数据，不需要交易解锁，也不应调用交易解锁 API。

## 可选私有知识库

如果用户希望结合自己的学习资料，应引导用户在公开仓库外建立私有 RAG/知识库，并可帮助建立本地索引。原始 PDF、截图、指标、笔记和私有命名应留在私有库中；只有抽象后的通用经验可以在用户明确要求时写入 skill。允许保留 gamma、GEX、dealer hedging、FVG、KDJ、MACD、RSI、VWAP、Vegas 等通用概念；不要写入个人仓位、本地路径、原创策略名、私有人名/handle、私有文档名或独特标签。

## 公开安全说明

这个 skill 可以放在公开仓库中。请不要提交 moomoo 账号、OpenD 日志、个人截图、私有行情输出、`.env`、token、`Stocks` 原始资料或任何含有登录信息的文件。

本 skill 输出仅用于个人研究，不构成投资建议。Gamma/GEX 是估算框架，不等于真实做市商持仓。
