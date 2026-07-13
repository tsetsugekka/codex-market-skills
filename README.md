# Codex Market Skills

<p align="center">
  <strong>面向交易、投资研究、市场异动解释和财经日历管理的 Codex Skill Suite。</strong>
</p>

<p align="center">
  <a href="README.md">中文</a> |
  <a href="README.en.md">English</a> |
  <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <code>Codex Skill</code> · <code>CN / JP / US Markets</code> · <code>Public-safe</code> · <code>No secrets</code>
</p>

---

> 面向交易、投资研究、市场异动解释和财经日历管理的 Codex Skill Suite。

![Codex](https://img.shields.io/badge/Codex-Skill%20Suite-4f46e5)
![Markets](https://img.shields.io/badge/Markets-CN%20%7C%20JP%20%7C%20US-22c55e)
![Language](https://img.shields.io/badge/Language-%E4%B8%AD%E6%96%87-blue)
![Secrets](https://img.shields.io/badge/Secrets-not%20included-critical)

## 这是做什么的

Codex Market Skills 是一组面向交易、投资研究和市场日程管理的 Codex skills。同一个 GitHub 项目中保存多个边界清晰、可单独安装和维护的市场工作流。

主要覆盖 4 类任务：

| 方向 | 覆盖内容 |
| --- | --- |
| 个股异动 | A 股、日股、美股/ETF 的上涨、下跌、放量、涨停、盘前盘后异动原因分析 |
| 题材与情绪 | A 股题材强弱、短线情绪周期、论坛/掲示板/社区温度、主线与预期差 |
| 宏观与结构 | 宏观快讯、大盘 tape、技术结构、支撑压力、gamma/GEX、0DTE 情景表 |
| 日历与报告 | 美股/日股财报、宏观事件、央行事件、市场策略报告、收盘复盘 |

## Skill 总览

| Skill | 用途 | 关键依赖 |
| --- | --- | --- |
| [`market-calendar-google`](docs/market-calendar-google.md) | 整理财报、宏观数据、央行事件、拍卖和其他财经事件，并写入 Google Calendar | 必需：`google-calendar:google-calendar` |
| [`jp-stock-move-reason`](docs/jp-stock-move-reason.md) | 分析日本股票急涨、急跌、放量和掲示板/新闻驱动 | 无 |
| [`cn-stock-move-reason`](docs/cn-stock-move-reason.md) | 分析 A 股涨停、跌停、炸板、放量和市场/板块/个股共振 | 可选：`mx-data`、`mx-search`、`mx-xuangu`、`mx-zixuan` |
| [`cn-market-tape`](docs/cn-market-tape.md) | 盘中/盘后计算题材强弱、板块资金流、涨停池和机构调研 | 题材必需：`mx-zixuan`、`mx-xuangu`、`mx-search`；其他模块优先：`mx-data` |
| [`stock-sentiment-analysis`](docs/stock-sentiment-analysis.md) | 给其他股票 skill 复用的公开安全情绪面分析框架 | 可选：东方财富妙想、moomoo 社区样本增强 |
| [`macro-news-check`](docs/macro-news-check.md) | 在个股、指数、技术或 gamma 分析需要时检查宏观和大盘背景 | 无 |
| [`market-daily-strategist`](docs/market-daily-strategist.md) | 输出美股、日股、A 股盘前策略、收盘复盘和长线推荐 | 可选：市场数据、异动、技术、情绪、gamma skill |
| [`us-stock-move-reason`](docs/us-stock-move-reason.md) | 结合 moomoo 新闻、摘要、社区、资金、期权、技术异常分析美股/ETF 异动 | 可选但推荐：moomoo 系列 skill |
| [`us-stock-gamma-moomoo`](docs/us-stock-gamma-moomoo.md) | 通过 moomoo OpenD 分析美股期权 gamma/GEX、gamma wall、0DTE 情景表 | 必需：本机 moomoo OpenD、Python SDK `moomoo` |
| [`stock-technical-analysis`](docs/stock-technical-analysis.md) | 分析美股、日股、A 股技术结构、支撑压力、量价和指标 | 可选：东方财富妙想、`moomoo-technical-anomaly` |

## 特点

- **多市场同仓管理**  
  A 股、日股、美股、ETF、指数、财报日历、宏观事件和期权结构放在同一个 skill suite 中，但每个 skill 都保持清晰边界。

- **公开安全设计**  
  仓库只保存通用工作流、公开安全的规则和脚本；不提交个人关注列表、凭据、API key、`.env`、私有 RAG、运行缓存或私有输出。

- **证据优先的交易研究流**  
  每个异动分析都优先区分确认催化、市场思惑、论坛热度、技术确认、宏观放大器和背景噪音。

- **可协同调用**  
  个股异动、情绪周期、宏观 tape、技术分析和 gamma 结构可以按需组合，避免单一信号解释全部价格变化。

- **中文报告优先**  
  默认面向中文交易研究和盘中决策场景；英文、日文 README 作为安装和公开说明辅助。

## 适用入口

| 用户想问 | 建议入口 |
| --- | --- |
| “这只 A 股为什么涨停/跌停/炸板？” | `cn-stock-move-reason` |
| “这只日股是新闻驱动还是掲示板思惑？” | `jp-stock-move-reason` |
| “这只美股为什么盘前/盘后异动？” | `us-stock-move-reason` |
| “A 股今天哪些题材最强、最弱，资金去了哪些板块？” | `cn-market-tape` |
| “现在的涨停池和机构调研热度如何？” | `cn-market-tape` |
| “这个票是不是主线启动、高潮分歧或退潮反抽？” | `stock-sentiment-analysis` |
| “有没有宏观或大盘因素影响？” | `macro-news-check` |
| “这只股票现在技术面怎么看？” | `stock-technical-analysis` |
| “SPX/SPY/个股期权 gamma 结构怎么看？” | `us-stock-gamma-moomoo` |
| “写一份盘前策略或收盘复盘。” | `market-daily-strategist` |
| “整理本周财报和财经事件到日历。” | `market-calendar-google` |

## Skill 详情

<details>
<summary><code>market-calendar-google</code> - 市场日历整理</summary>

整理美股财报、日股财报、中美日宏观数据、央行事件、拍卖和其他重要财经事件，并按用户规则写入 Google Calendar。

依赖：必需 - `google-calendar:google-calendar`。

协同调用：无。

适用场景：

- 整理本周或下周 Earnings Whispers 美股财报图。
- 根据关注列表筛选美股或日股财报。
- 整理中美日四星以上财经事件。
- 把事件按用户本地时间写入 Google Calendar，并避免重复。

</details>

<details>
<summary><code>jp-stock-move-reason</code> - 日股异动原因</summary>

针对用户输入的日本股票代码，抓取 Yahoo Finance 实时板、Yahoo 掲示板、Yahoo/Kabutan/Traders 新闻以及基础指标，让 Codex 分析个股异动理由。

依赖：无。

协同调用：`stock-sentiment-analysis`、`macro-news-check`、`stock-technical-analysis`。

适用场景：

- 分析某只日股为什么急涨、急跌或突然放量。
- 区分新闻确认的催化和 Yahoo 掲示板上的市场思惑。
- 查看当前涨跌幅、市值、PER/PBR、信用倍率、掲示板温度等辅助信息。

</details>

<details>
<summary><code>cn-stock-move-reason</code> - A 股异动原因</summary>

针对用户输入的单只 A 股代码，抓取东方财富公开行情、公告、股吧/资讯帖，并结合搜狐指数/板块页面与 A 股涨跌家数背景，让 Codex 分析个股异动理由、是否大盘/板块/个股共振，以及短线情绪周期位置。

依赖：可选 - `mx-data`、`mx-search`、`mx-xuangu`、`mx-zixuan`（东方财富妙想增强）。

协同调用：`stock-sentiment-analysis`、`macro-news-check`、`stock-technical-analysis`。

适用场景：

- 分析某只 A 股为什么涨停、跌停、炸板或突然放量。
- 区分公告/业绩确认催化和股吧题材思惑。
- 结合大盘指数、行业/概念板块和涨跌家数，判断是市场共振、板块主线，还是个股独立催化。
- 按冰点、修复/潜伏、启动、加速、高潮、高位分歧/分化、退潮判断短线情绪阶段。

</details>

<details>
<summary><code>cn-market-tape</code> - A 股盘面数据</summary>

统一处理 A 股盘中/盘后的题材强弱、板块主力资金流、涨停池和机构调研。题材模块读取本地题材映射和中文标签，用东方财富妙想行情按映射权重计算 TOP10/BOTTOM10；其他模块优先使用妙想聚合数据，字段不支持或不完整时切换到公开聚合备用源，并报告数据时间、口径和来源变化。

日内重复查询资金流时，自动与上一次同口径快照比较，仍以当前值、上次值、变动额和排名变化的表格返回。

依赖：题材强弱必需 - `mx-zixuan`、`mx-xuangu`、`mx-search`；其他模块优先 - `mx-data`；机构调研使用本 skill 内置聚合脚本。

协同调用：`cn-stock-move-reason`、`macro-news-check`，仅在用户要求解释原因时调用。

适用场景：

- 盘中/盘后输出题材强弱 TOP10/BOTTOM10。
- 按“主力净流入 Top10 / 主力净流出 Top10”格式输出板块资金流。
- 查看涨停数量、连板梯队、炸板和行业/题材分布。
- 查看最近交易日或历史窗口的机构调研热度；没有对应历史数据时明确说明不支持。
- 不默认写文件；备用接口遇到限流、封禁或不稳定时报告 host、接口类别和错误。

</details>

<details>
<summary><code>stock-sentiment-analysis</code> - 情绪面框架</summary>

给其他股票 skill 复用的情绪面分析框架，用于判断 A 股情绪周期、主线/跟随、预期差、论坛/掲示板温度、拥挤交易和跨市场 risk-on/risk-off。公开版不包含私人 RAG、个人标签或原始资料。

依赖：可选 - `mx-data`、`mx-search`、`mx-xuangu`（A 股证据、题材成分和筛选增强）；`mx-zixuan`（仅用户明确要求自选股任务时）；`moomoo-comment-sentiment`（美股社区样本增强）。

协同调用：`cn-stock-move-reason`、`jp-stock-move-reason`、`us-stock-move-reason`、`stock-technical-analysis`、`us-stock-gamma-moomoo`。

适用场景：

- 把股吧/掲示板热度、新闻预期差、板块广度和图形确认整合成情绪结论。
- 给 `cn-stock-move-reason`、`jp-stock-move-reason`、`us-stock-move-reason`、`stock-technical-analysis`、`us-stock-gamma-moomoo` 提供统一情绪框架。
- 在用户指定私有 RAG 目录时，可帮助用户建立本地索引，只记录主题、来源别名、页码/slide 范围、关键词和公开安全摘要；不把私有材料写入公开仓库。

</details>

<details>
<summary><code>macro-news-check</code> - 宏观快讯检查</summary>

给其他市场 skill 调用的宏观快讯检查工具，只在个股、指数、技术分析或 gamma 分析确实需要当前宏观/大盘背景时使用。用户只需要问是否有大盘、宏观、跨资产或风险情绪影响；skill 会自动选择公开快讯和市场确认来源。

依赖：无。

协同调用：无。

适用场景：

- 判断个股或指数异动是否受利率、汇率、央行、经济数据、商品、地缘或大盘 risk-on/risk-off 影响。
- 给 `cn-stock-move-reason`、`jp-stock-move-reason`、`stock-technical-analysis`、`us-stock-gamma-moomoo` 提供宏观 tape。
- 把 2-5 条关键快讯转化为对当前标的的主因/放大器/背景噪音判断。

</details>

<details>
<summary><code>market-daily-strategist</code> - 市场策略报告</summary>

面向美股、日股和 A 股的中文市场策略报告路由层，覆盖盘前策略、收盘复盘和单只长线推荐。它按用户意图读取对应市场和时段的 reference，并把宏观、异动原因、情绪周期、技术结构和可用的本地行情工具压缩进一份决策导向报告。

依赖：可选 - `mx-data`、`mx-search`、`mx-xuangu`（A 股行情、资讯、板块/概念成分增强）；`mx-zixuan`（仅用户明确要求自选股任务时）；官方 moomoo 新闻、摘要、评论、资金、期权和技术异动 skill（美股报告增强）。

协同调用：`macro-news-check`、`stock-sentiment-analysis`、`stock-technical-analysis`、`cn-stock-move-reason`、`jp-stock-move-reason`、`us-stock-move-reason`、`us-stock-gamma-moomoo`。

适用场景：

- 写美股、日股或 A 股盘前策略。
- 写美股、日股或 A 股收盘复盘。
- 推荐一只美股、日股或 A 股/ETF/LOF，并给出买点、风险和验证条件。

</details>

<details>
<summary><code>us-stock-move-reason</code> - 美股异动原因</summary>

针对用户输入的美股或 ETF，结合官方 moomoo 新闻、摘要、社区评论、资金异动、期权异动和技术异动，以及本仓库的 gamma、技术、情绪和宏观 skill，分析股价为什么上涨、下跌、盘前跳空或盘后异动。

依赖：可选但推荐 - `moomoo-news-search`、`moomoo-stock-digest`、`moomoo-comment-sentiment`、`moomoo-capital-anomaly`、`moomoo-derivatives-anomaly`、`moomoo-technical-anomaly`；可选 - 本机 moomoo OpenD 和 Python SDK。

协同调用：`us-stock-gamma-moomoo`、`stock-technical-analysis`、`stock-sentiment-analysis`、`macro-news-check`。

适用场景：

- 分析 DELL、NVDA、TSLA 等美股为什么急涨、急跌或盘前/盘后异动。
- 区分财报/指引/评级/订单等确认催化和社区思惑。
- 检查美股适用的期权大单、IV、期权情绪、资金、短卖和技术异动。
- 对 SPY/QQQ/SPX 相关问题，把宏观、技术和期权/gamma 结构合并判断。

</details>

<details>
<summary><code>us-stock-gamma-moomoo</code> - 期权 Gamma 结构</summary>

通过 moomoo OpenD 获取美股/美股期权数据，让 Codex 分析 gamma/GEX、gamma wall、gamma flip、SPX/SPY/ES 盘中结构，以及 0DTE 期权情景表。该 skill 需要本机运行 moomoo OpenD；如果环境不存在，应先引导安装或启动 OpenD。

依赖：必需 - 本机 moomoo OpenD、Python SDK `moomoo`；可选 - `moomoo-derivatives-anomaly`（美股期权异动、大单、IV、PCR 和期权情绪扫描）。

协同调用：`macro-news-check`、`stock-technical-analysis`、`stock-sentiment-analysis`、`us-stock-move-reason`。

适用场景：

- 分析普通美股或美股 ETF 的期权 gamma 结构，并可用官方 moomoo 期权异动扫描辅助识别大单、IV、PCR 和期权情绪。
- 分析 `.SPX`/SPXW 指数期权结构；如果拿不到指数实时行情或期权链，则用 SPY 期权、ES/CFD 或用户提供的指数锚进行换算并明确说明。
- 对 0DTE call/put 生成“时间 x 标的价位”的理论价值表，用于评估回本、止盈或止损点。
- 输出以文字结论、列表和文本表格为主；盘中重复询问时，结合本交易日此前同一对话中的 gamma 结果判断点位迁移和强弱变化。

</details>

<details>
<summary><code>stock-technical-analysis</code> - 技术分析</summary>

针对美股、日股和 A 股做技术分析，重点看趋势结构、支撑压力、量价、KDJ/MACD/RSI、Vegas 通道、分时确认，以及“能不能到某个价位”的盘中判断。

依赖：可选 - `mx-data`、`mx-search`、`mx-xuangu`（A 股行情、资讯、板块/概念成分和技术筛选增强）；`mx-zixuan`（仅用户明确要求自选股任务时）；`moomoo-technical-anomaly`（美股官方技术异动扫描）。

协同调用：`macro-news-check`、`stock-sentiment-analysis`、`cn-stock-move-reason`、`jp-stock-move-reason`、`us-stock-move-reason`、`us-stock-gamma-moomoo`。

适用场景：

- 判断当前走势是强趋势延续、空中加油候选、回踩确认、冲高回落、高位分歧，还是破位反抽。
- 区分 touch、break、tradable hold，避免把一根影线误判为有效突破。
- 读取 moomoo/Yahoo/券商图表或截图，给出当前读数、技术结构、量价动能和下一验证点。
- 与日股/A 股异动原因或美股 gamma skill 配合，判断催化是否被图形确认。
- 对美股，把官方技术异动当作提示，再按趋势位置、VWAP/均线、量价、动能背离、支撑压力和失败突破判断是否有效。

</details>

## 安装

在 Codex 里直接发送这个仓库链接，并说明要安装全部或指定 skill：

```text
请从 https://github.com/tsetsugekka/codex-market-skills 安装我需要的 Codex skills。
```

如果只需要其中一个，可以把 skill 名一起告诉 Codex，例如 `stock-technical-analysis` 或 `cn-market-tape`。

## 示例请求

```text
整理下周 Earnings Whispers 财报图，并添加到 Google Calendar。
```

```text
整理本周中美日四星以上财经事件，加入 Google Calendar。
```

```text
分析一下 6758 今天异动原因。
```

```text
看一下 6217 是新闻驱动还是掲示板思惑。
```

```text
分析一下 300750 今天是公告驱动还是情绪题材。
```

```text
看看当前 A 股题材强弱，显示 TOP10 和 BOTTOM10。
```

```text
盘中看一下 A 股哪些题材涨得好，哪些题材最差。
```

```text
分析一下这只股票现在是主线启动、高潮分歧，还是退潮反抽。
```

```text
这个票今天有没有大盘或宏观原因影响？
```

```text
写一份今天 A 股收盘复盘，重点看主线、明天风险和可操作方向。
```

```text
查一下这只美股的 gamma，阻力位和这周可能去的位置。
```

```text
算一下 SPXW 0DTE 7370C 在不同时间和 SPX 点位下的理论价值。
```

```text
这个股票现在技术面怎么看，压力位和支撑位在哪里？
```

## 安全边界

- `market-calendar-google` 会在用户明确要求时使用 Google Calendar 连接器创建或更新日历事件。
- `jp-stock-move-reason` 只读取公开网页/API，不读取 token，不写入外部服务，不调用 Gemini/OpenAI API。
- `cn-stock-move-reason` 只读取东方财富、搜狐证券等公开网页/API，不读取 token，不写入外部服务，不调用 Gemini/OpenAI API。
- `cn-market-tape` 的题材强弱必须使用东方财富妙想 `mx-zixuan` 和 `mx-xuangu`；只查询自选股，不自动添加、删除或修改自选股。资金流、涨停池和机构调研优先使用妙想聚合查询，备用接口必须批量、低频、带随机等待，不提交 `MX_APIKEY`、完整自选股列表、题材映射本地缓存、原始 API 响应或运行缓存。
- `stock-sentiment-analysis` 只保存公开安全的通用情绪框架；不应提交私人 RAG、个人标签、原始笔记、截图或交易日志。
- `macro-news-check` 只读取公开宏观快讯页面/Feed/接口；不读取登录 cookie、token、账号数据或私有研究资料，不复制长篇新闻正文。
- `market-daily-strategist` 是报告路由和综合层；本地/私有行情工具只作为可选增强，不应把个人关注列表、私有输出或工具缓存提交到公开仓库。
- `us-stock-move-reason` 只保存公开安全的美股异动分析流程；官方 moomoo skill 和 OpenD 只作为运行时数据层，不应提交账号、OpenD 日志、原始社区抓取、私有输出或个人交易记录。
- `us-stock-gamma-moomoo` 使用本机 moomoo OpenD 行情接口，不调用交易解锁接口；公开版不依赖私有 RAG，不应提交个人账号、OpenD 日志、截图、私有行情输出、原创策略名或私有人名/handle。
- `stock-technical-analysis` 只保存通用技术分析规则；公开版不依赖私有 RAG，不应提交个人仓位、交易计划、截图原图、私有研究路径、专有指标名、原创策略名或私有人名/handle。
- 不要把个人关注列表、凭据、API key、`.env`、私有 RAG、运行缓存或私有输出提交到本仓库。

## 仓库结构

```text
skills/
  market-calendar-google/
    SKILL.md
    agents/openai.yaml
  jp-stock-move-reason/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    scripts/stock_move_sources.py
  cn-stock-move-reason/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    scripts/stock_move_sources.py
  cn-market-tape/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
  stock-sentiment-analysis/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    references/sentiment-framework.md
  macro-news-check/
    SKILL.md
    agents/openai.yaml
  market-daily-strategist/
    SKILL.md
    references/
  us-stock-move-reason/
    SKILL.md
    agents/openai.yaml
  us-stock-gamma-moomoo/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/gamma_report.py
    scripts/option_scenario_table.py
  stock-technical-analysis/
    SKILL.md
    agents/openai.yaml
    references/
docs/
  market-calendar-google.md
  jp-stock-move-reason.md
  cn-stock-move-reason.md
  cn-market-tape.md
  macro-news-check.md
  market-daily-strategist.md
  stock-sentiment-analysis.md
  us-stock-move-reason.md
  us-stock-gamma-moomoo.md
  stock-technical-analysis.md
shared/
  references/release-and-privacy.md
```

## 语言

- 中文：`README.md`
- 日本語：`README.ja.md`
- English: `README.en.md`
