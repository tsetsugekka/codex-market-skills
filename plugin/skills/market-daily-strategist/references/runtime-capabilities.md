# 按运行环境使用能力

同一插件面向 ChatGPT Web、ChatGPT 工作及 Codex。按本轮实际可见的 Skill、工具、连接和执行环境选择来源，不凭产品名称推断权限，也不把“已安装”当作“已连通”。某个 Web 对话没有工具，不代表工作任务或 Codex 也没有；反过来，某次本机调用成功也不证明所有宿主都可用。

## 发现与调用

1. 先复用用户资料、任务数据包和本轮已取得的证据。需要补充时，从当前 Skill 清单或宿主提供的发现工具中寻找与缺口匹配的能力。
2. 找到相关 Skill 后先读它的现行说明，通过它规定的入口确认所需运行环境、连接和数据权限，再按需查询。若能力由连接器或工具直接提供而没有同名 Skill，按该工具的现行合同调用，不能因缺少 Skill 名称拒绝可用能力。具备本机文件与执行工具时可使用已安装的本机 Skill；云端执行环境只访问其自身可见资源，不能推定能连接用户电脑。仅有网页工具时继续公开网页流程。
3. 只调用本轮需要的来源，不逐项探测所有供应商。没有安装、缺少权限或调用失败时，换用可用来源并保留数据缺口；不自动安装、登录、申请权限或修改凭据配置。限流或拒绝访问时停止该来源请求。

## 研究能力路由

| 研究缺口 | 已安装且可用时的候选 Skill |
| --- | --- |
| A股行情、资金、估值与财务 | `mx-data`；同花顺 `hithink-finance-market`、`hithink-finance-financials`、`hithink-finance-valuation` |
| 新闻、公告、研报与原因核验 | `mx-search`；`moomoo-news-search`、`moomoo-stock-digest` |
| 题材成分、条件筛选、涨跌停与异动 | `mx-xuangu`；同花顺 `hithink-finance-index`、`hithink-finance-special-data` |
| 行情、K线、分时及期权链 | `moomooapi`，按其说明核验 OpenD、SDK、连接及对应市场权限 |
| 资金、技术、衍生品异常及社区情绪 | 对应 `moomoo-capital-anomaly`、`moomoo-technical-anomaly`、`moomoo-derivatives-anomaly`、`moomoo-comment-sentiment` |

同花顺也可从已安装的 `hithink-finance` 入口按实际能力路由，执行规则以该环境的 Skill 为准。本插件不复制供应商命令、凭据位置或依赖安装步骤。

## 随包 Python

安装包包含以下标准库脚本，需 Python 3.10+。先定位实际安装目录、确认文件可读及执行能力，再用 `--help` 核对参数。文件被平台接受、当前会话能运行 Python、Python 能访问目标网站，是三个分别验证的条件。

| Skill / 脚本 | 用途 | 网络与副作用 |
| --- | --- | --- |
| 日股 `stock_move_sources.py` | 报价、新闻、掲示板采集及完整筛选 | 联网；Yahoo 临时限速状态；默认 stdout，可指定输出文件 |
| 日股 `pts_turnover_ranking.py` | 正盘/PTS 涨跌异动推定成交额排名 | 联网；同一 Yahoo 限速状态；stdout |
| 日股 `filter_forum.py` | 对已取得的单股评论执行同一筛选算法 | 不联网；只读输入 JSON、stdout |
| 日历 `fetch_sbi_jp_earnings.py` | 从 SBI 动态入口发现并读取日股财报日历 | 联网；stdout，不写日历 |
| 策略 `narrative_status.py` | 检查公开新闻索引时效并按市场整理 | 联网；stdout |
| Gamma `option_scenario_table.py` | 已知 IV、期限与价格情景的期权模型表 | 不联网；stdout；系统需可用的时区数据库 |

日股联网、离线与无执行能力的具体入口见[执行说明](../../jp-stock-move-reason/references/python-execution.md)。其他脚本的输入、方法与限制见对应 Skill。无 Python 时可以用可用网页/连接器取得证据，但不得宣称脚本或完整数值流程已经运行。完整 OpenD 采集器、供应商 Skill、SDK、凭据和行情权限不随包分发。

## 结果与权限

核对返回的市场、代码、日期、时区、复权、延迟和覆盖范围；本机缓存同样可能过期。使用真实返回值，不能因连接成功就声称已取得完整分时或期权数据。只有必要输入齐备且实际执行计算，才报告 GEX 等计算结果及假设。

本路由默认用于研究查询。真实或供应商模拟交易、账户/自选修改等写操作须有对应用户授权，并遵循被调用 Skill 的边界；Task 的 AI 模拟账本授权不等于券商下单授权。凭据由所用 Skill 的既有安全入口处理，不读取输出秘密值、不复制到插件或报告。

Scheduled Task 仍以当轮实际可见能力为准，不因普通对话或 Codex 能使用插件就推定定时任务也已加载。任务自身的输出、归档、模拟账本与授权范围保持优先；运行诊断仅在影响结论时于文末简述。
