---
name: cn-market-tape
description: 分析A股盘中或盘后题材强弱、板块资金、涨停结构、市场宽度和机构调研，使用可核验公开资料。
---

# CN Market Tape

## 跨环境执行

先按[环境能力路由](../market-daily-strategist/references/runtime-capabilities.md)发现当前会话已安装、已连接且有权限的 Skill、工具、网页和计算能力。OpenD/moomoo、妙想、同花顺等是可选数据能力；不能由 ChatGPT Web、工作环境或 Codex 的名称推定可用性。优先复用已取得且仍有效的资料。研究来源顺序、字段与计算方法不因环境不同而省略；缺能力时说明具体缺口，不宣称已采集或已计算。

此包按各 Skill 入口附带可移植 Python 脚本；可读取文件不等于能执行，能执行不等于能联网。先确认能力，再按环境路由选择随包脚本、可用扩展或公开网页；仅有用户资料时执行相同筛选与计算，无执行能力时按文字流程研究并标出未计算项。外部供应商采集器只在已安装且可用时调用。访问失败、限流与权限处理遵循当前工具及环境规则，不复制机器专用沙箱设置。实际加载所用的同包 Skill 和参考，不只在回答中提名字。

本插件用于研究，写日历、账户或交易需要对应授权。普通研究不自动访问私人自选或持仓，不修改自身、其他 Skill 或任务规则；自动任务保持自己的输出、归档和授权合同。用户指定的私人资料仅在本轮授权范围内使用，不写入插件。

统一处理 A 股盘中和盘后盘面数据。默认只抓用户请求的模块，不读取或修改用户自选股之外的账户数据，不把一日榜单、资金流和机构调研混成一个结论。

## Routing

先判断用户要的是盘中快照、收盘数据还是历史数据，再选择模块：

1. `题材强弱`、`题材 TOP10/BOTTOM10`：使用本 skill 的加权题材流程。
2. `板块流入流出`、`主力净流入/净流出`：默认按题材/概念板块处理，并直接使用 `push2delay.eastmoney.com` 聚合公开接口；该接口失败后只切换一次到 `push2.eastmoney.com`。只有用户明确说“行业板块/行业”时才切换到行业板块口径。`mx-data` 仅用于用户明确要求 MX 或公开聚合接口缺少的补充字段，不再作为该模块的前置调用。
3. `涨停池`：先尝试 MX 或已有的聚合涨停池接口；不要逐只股票抓取涨停状态。
4. `机构调研`：当前/最近交易日优先运行已安装扩展的机构调研聚合能力或公开调研记录；历史请求优先使用公开历史调研热度数据，找不到对应日期或字段时明确声明不支持。

若用户只要求“盘中快照”，不要自动抓股吧、新闻或历史数据；若用户要求“为什么”或“复盘”，再按需要调用 `mx-search`、`cn-stock-move-reason` 和 `macro-news-check`。

### DTM 接口

DTM 数据优先使用 `https://daytrading.monster/api-docs/` 中的正式接口：

- `https://daytrading.monster/api/chinastock-anomaly`：最新涨跌题材 Top10、涨停概念 Top8、当日小时榜单、完整异动原因和涨停池。逐块核对交易日和时间；该榜单与下文 MX 成分加权榜是不同口径，不能混合排名或当作同口径历史快照。
- `https://daytrading.monster/api/themes?market=cn`：A 股题材成员、权重、中文名称与依据及阶段表现；阶段涨跌与 `price_dates` 不作为实时行情。此接口用于生成映射缓存；加权题材榜继续读取 MX 行情，资金榜与分时按 Module 2 的来源规则执行。

接口正文是 JSON，即使 Content-Type 为 `text/plain`。不读取 DTM 机构调研数据；机构调研继续使用既有流程。

## Module 1: Theme Strength

### Theme universe

题材映射从 `https://daytrading.monster/api/themes?market=cn` 的 `themes[].constituents[]` 提取成员和权重，中文标签取 `theme_name_zh`。如使用已保存映射，先检查日期与完整性；超过7天刷新，失败时明确旧映射状态。没有有效映射就停止此模块，不按行业名发明题材池。

只保留 `market == "CN"`、`theme != "未分類"` 的行。每行至少需要 `code`、`theme` 和 `weight`；重复的股票-题材关系按独立权重参与计算。中文标签取公开接口提供的中文标签。

### Quotes and aggregation

1. 提取去重后的 A 股代码，但保留所有股票-题材关系用于加权。
2. 用户明确要求使用自选且已授权时，可调用 `mx-zixuan` 一次作快速覆盖层；普通研究直接批量取得成分行情。读取 `SECURITY_CODE`、`SECURITY_SHORT_NAME`、`NEWEST_PRICE`、`CHG` 和 `dateMsg`。
3. 对缺失代码按最多 50 只一批调用 `mx-xuangu`，批次串行。遇限流或 HTTP 503 停止该来源，遵循当前工具的重试规则。
4. 合并行情时优先使用 `mx-zixuan`，用 `mx-xuangu` 补齐；若日期不一致，报告混合日期风险。
5. 按下式计算每个题材的加权涨跌幅：

```text
theme_return = sum(theme_weight * stock_chg_pct) / sum(theme_weight)
```

`CHG` 按百分数处理，例如 `10.03` 表示 `+10.03%`。TOP 榜列出 `weight * CHG` 最大的贡献股，BOTTOM 榜列出最小的拖累股。

### Theme interpretation

需要判断持续性、拥挤度、主线、反抽或退潮时，读取 [theme-mainline-lifecycle](../../../skills/cn-market-tape/references/theme-mainline-lifecycle.md)。生命周期只解释榜单质量，不替代加权排名。

默认只检查 TOP3 题材：每个题材选涨幅最高的代表股，结合股吧/讨论发现和 `mx-search` 资讯，区分确认消息、市场思惑、海外映射和个股独立逻辑，并给出“较高/中等/较低”确定度。

## Module 2: Theme/Board Money Flow

### Source priority

先确定板块命名空间：用户说“板块/题材/概念”时默认使用题材/概念板块；只有明确说“行业板块/行业”时才使用行业板块。随后直接请求 `push2delay.eastmoney.com` 聚合公开接口，并校验目标板块名称、板块级资金字段和目标交易日；默认接口失败后只切换一次到 `push2.eastmoney.com`。`mx-data` 仅用于用户明确要求 MX 或聚合接口缺少的补充字段。不要逐板块、逐股票循环抓取。

公开备用接口的命名空间固定为：概念/题材板块 `m:90+t:3`；行业板块 `m:90+t:2`。每次输出必须注明“概念板块”或“行业板块”，不得把两个宇宙混在同一张榜或同一组快照比较中。

备用源的字段、请求顺序、超时和错误处理见 [market-tape-source-routing](references/market-tape-source-routing.md)。排名榜必须分别获取净流入方向和净流出方向；不能只取按降序返回的第一页，再把末尾几行误称为净流出。若接口声明的总数超过本次返回条数，要记录分页/返回上限风险。金额原始值按元解析后再统一换算为亿元，并保留接口更新时间。同一 host 连续请求超过 3 次后必须加入 8-20 秒随机等待；已出现 HTTP 429/403/5xx、超时、DNS 失败或连接重置时，立即报告 host、endpoint family 和错误，停止继续增加该 host 的请求量。

### Required output

盘中/盘后资金流必须按以下口径输出：

```text
数据时间：YYYY-MM-DD HH:MM；资金口径：主力净流入/净流出；来源：MX 或备用聚合源。

主力净流入 Top10
排名 | 题材/概念板块 | 主力净流入

主力净流出 Top10
排名 | 题材/概念板块 | 主力净流出
```

金额必须带单位，优先统一为亿元；同时给出市场宽度或指数快照（如可得）。说明榜单是当前快照还是收盘值，且不要把两个榜单的金额相加：不同板块标签可能重叠，资金流也可能按不同板块口径重复统计。

如果只获得部分板块或只获得净流入方向，明确标注“不完整”，不要补造另一张榜。

### Intraday minute flow and theme/sector chart SOP

When the user asks for `分时流入流出`、`分钟级资金`、`资金折线图`、`资金曲线` or asks to see the intraday turning point of a named sector/theme, follow the full SOP in [intraday-flow-chart-sop](references/intraday-flow-chart-sop.md). The short version is:

1. Disambiguate the object first. `融资融券` can mean the `融资融券` concept board or the market-wide margin-financing/margin-trading account statistics. The former can use minute-level board fund-flow data; the latter is generally an exchange daily summary and must not be presented as a minute chart.
2. Resolve the exact board code from an aggregate board list. For an unqualified `板块/题材/概念` request, use the concept universe `m:90+t:3`; use the industry universe `m:90+t:2` only for an explicit `行业/行业板块` request. Do not guess a code, and do not mistake a constituent-stock response for a board row. In the same run, accept a minute series only when its `data.name` exactly confirms the requested board and namespace.
3. Query the current-day minute series from `push2delay.eastmoney.com` with `klt=1` and `lmt=240`. Preserve provider timestamps and trading-session gaps in the data; never interpolate the lunch break or missing points. For afternoon chart updates, compress the lunch interval on the display by default, draw morning and afternoon as separate paths, and add a clear 11:30/13:01 session divider. Record the series' latest point separately from the ranking snapshot's update time because the minute endpoint may lag. If the default host fails, switch once to `push2.eastmoney.com`; if both fail, report both host/endpoint results and stop increasing request volume.
4. Interpret `f51` as timestamp, `f52` as cumulative main net inflow, `f53`/`f54` as small/medium-order net flow, and `f55`/`f56` as large/super-large-order net flow. Parse yuan first, then convert to亿元. Check that `f52` approximately reconciles to `f55 + f56` before charting.
5. For one board, plot cumulative `f52` with a visible zero line, y-axis unit, date/time, source, cumulative label, low/high, zero crossings, and latest point. When comparing “现在和上午收盘”, use only the exact 11:30 minute point as the morning close and show current, 11:30, and the difference. Do not call an earlier saved snapshot “morning close”. For multiple themes/boards, use one shared time axis; use 分面图 when scales differ and do not normalize away the yuan/亿元 meaning. The chart is supplemental to the latest snapshot table.
6. Only when the user explicitly asks for “每分钟变化/增量” calculate adjacent-point differences of `f52`; render and label that series separately from the cumulative curve.

The default chart read should state whether the tape is persistent outflow, early outflow then recovery, early inflow then distribution, or two-way high-level divergence. A positive latest point after a deep intraday drawdown is a recovery path, not automatically a full-day inflow trend. If the endpoint is empty, stale, non-JSON, rate-limited, timed out, or otherwise unstable, report the host/endpoint family and stop increasing request volume; return the validated snapshot table or state that the chart is unavailable.

### Intraday snapshot comparison

同一交易日内再次查询资金流时，自动读取本次会话中的上一次结果；若会话中没有，则读取运行时快照缓存。缓存只保存聚合榜单、交易日、数据时间、来源、资金口径和单位，不保存原始响应或账户数据。有可用会话存储时才保存聚合快照，不假定宿主有持久本地缓存；不写入插件或源码。

只有当交易日、资金口径、来源、单位、板块命名空间（概念/行业）、板块宇宙和数据时间范围一致时才做数值比较。MX 切换到备用源、榜单口径变化或日期不一致时，仍输出当前表，但在表头写明“上次快照不可比”，不能把不同口径的数字相减。分时图比较优先使用相同时间点；只能取得各自最新点时，明确写出时间不一致和接口滞后。

首次查询时保存当前快照，并在表头写 `上次快照：无`。再次查询时，仍然只输出两张表，但列改为：

```text
主力净流入 Top10（当前 vs 上次）
当前排名 | 板块 | 当前净流入 | 上次排名 | 上次净流入 | 变动额

主力净流出 Top10（当前 vs 上次）
当前排名 | 板块 | 当前净流出 | 上次排名 | 上次净流出 | 变动额
```

当前或上次未进入对方 Top10 的板块使用 `—`，并标注 `新入榜` 或 `出榜`；`—` 不等于零，不据此计算虚假的变动额。表格之后只补一行数据状态，例如 `上次快照：10:32；当前：11:18；可比；来源：MX。` 查询成功后再写入当前快照，失败时不得覆盖上一次快照。

## Module 3: Limit-up Pool

优先查询当天聚合涨停池，校验交易日期 `qdate` 与当前请求日期。输出至少包括：

- 涨停总数、有效普通涨停数、跌停数（接口提供时）。
- 最高连板数，以及 2 板及以上的数量（接口提供时）。
- 炸板数、封板率、封单金额或成交额（接口提供时）。
- 连板梯队和行业/题材分布。
- 用户点名或与当前主线有关的重点股票，可列名称、代码、连板数、首次/最后封板时间和炸板次数。

区分“涨停池统计”和“涨停个股原因”。只有用户要求原因时，才对重点股票调用 `cn-stock-move-reason`；不要把聚合池扩展成逐只新闻抓取。

若盘中接口返回的是动态池，写明统计时间；盘后以收盘快照为准。日期字段缺失或不是目标交易日时，标记数据日期风险。

## Module 4: Institutional Survey

当前或最近交易日：使用可用的聚合工具或 MX 查询调研记录，按既有机构调研口径输出股票、行业和周度热度。

历史请求：

1. 优先使用公开历史调研热度数据或对应的历史 JSON 快照。
2. 校验目标日期/日期区间、`RECEIVE_START_DATE` 和数据生成时间。
3. 若历史源没有对应日期、字段或完整窗口，直接写“尚不支持该时间/数据”，不得用当前快照冒充历史数据。

## Combined workflow

1. 先列出本次需要的模块和数据时间，避免无关抓取。
2. 题材模块先刷新/读取映射，再按实际可用能力批量取同口径行情；非MX来源明确标注，不与MX快照混比。
3. 资金流按 Module 2 优先公开聚合接口；涨停池和调研按各自路由选择可用聚合来源，串行访问并随机等待。
4. 每个模块返回后先校验日期、字段完整性和数据来源，再合并结论。
5. 盘中报告标记 `盘中快照`，盘后报告标记 `收盘快照`；历史报告标记数据窗口。
6. 若某一来源失败，报告失败的 host/endpoint family、错误类型和切换后的来源；不要重复轰击已不稳定的接口。

## Default output order

用户未指定顺序时，按以下顺序输出：

1. 数据状态和时间。
2. 市场宽度/指数简表（可得时）。
3. `题材强弱 TOP10/BOTTOM10`。
4. `主力净流入 Top10` 和 `主力净流出 Top10`。
5. `涨停池`。
6. `机构调研`。
7. 只在用户要求时补充 TOP3 题材驱动、消息、技术或操作风险。

题材表默认列：`排名 | 题材 | 加权涨跌幅 | 主要贡献/拖累`。

资金表默认列：`排名 | 题材/概念板块 | 主力净流入/净流出`；用户明确要求行业时改为 `行业板块`。

始终用中文回答。说明每个数字是实时、延迟、盘后还是历史数据。默认不写输出文件，不提交 API key、cookie、账户标识、完整自选股列表、原始响应或运行缓存。

## Safety

- `mx-zixuan` 只查询，不添加、删除或修改自选股。
- 不把用户的个人持仓、自选股、私有调研资料或账户数据写入本仓库。
- 不把不同源、不同时间、不同统计窗口的数字直接拼接成一个精确结论。
- 输出仅用于市场研究，不构成投资建议。
