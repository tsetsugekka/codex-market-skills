# Codex Market Skills

Codex Market Skills 是一组面向交易、投资研究和市场日程管理的 Codex skills。项目原先只包含 `market-calendar-google`，现在扩展为一个多 skill 仓库：同一个 GitHub 项目中保存多个边界清晰、可单独安装和维护的市场工作流。

## 当前包含的 skills

### [`market-calendar-google`](docs/skills/market-calendar-google.md)

整理美股财报、日股财报、中美日宏观数据、央行事件、拍卖和其他重要财经事件，并按用户规则写入 Google Calendar。

依赖：必需 — `google-calendar:google-calendar`。

适用场景：

- 整理本周或下周 Earnings Whispers 美股财报图。
- 根据关注列表筛选美股或日股财报。
- 整理中美日四星以上财经事件。
- 把事件按日本时间写入 Google Calendar，并避免重复。

### [`jp-stock-move-reason`](docs/skills/jp-stock-move-reason.md)

针对用户输入的日本股票代码，抓取 Yahoo Finance 实时板、Yahoo 掲示板、Yahoo/Kabutan/Traders 新闻以及基础指标，让 Codex 分析个股异动理由。

依赖：可选 — `stock-sentiment-analysis`、`macro-news-check`、`stock-technical-analysis`（按掲示板/新闻/价格线索协同分析）。

适用场景：

- 分析某只日股为什么急涨、急跌或突然放量。
- 区分新闻确认的催化和 Yahoo 掲示板上的市场思惑。
- 查看当前涨跌幅、市值、PER/PBR、信用倍率、掲示板温度等辅助信息。

### [`cn-stock-move-reason`](docs/skills/cn-stock-move-reason.md)

针对用户输入的单只 A 股代码，抓取东方财富公开行情、公告、股吧/资讯帖，并结合搜狐指数/板块页面与 A 股涨跌家数背景，让 Codex 分析个股异动理由、是否大盘/板块/个股共振，以及短线情绪周期位置。

依赖：可选 — `mx-data`、`mx-search`、`mx-xuangu`、`mx-zixuan`（东方财富妙想增强）；`stock-sentiment-analysis`、`macro-news-check`、`stock-technical-analysis`（按问题协同分析）。

适用场景：

- 分析某只 A 股为什么涨停、跌停、炸板或突然放量。
- 区分公告/业绩确认催化和股吧题材思惑。
- 结合大盘指数、行业/概念板块和涨跌家数，判断是市场共振、板块主线，还是个股独立催化。
- 按冰点、修复/潜伏、启动、加速、高潮、高位分歧/分化、退潮判断短线情绪阶段。

### [`cn-theme-strength-mx`](docs/skills/cn-theme-strength-mx.md)

读取随 skill 打包的 `/themes` 股票-题材映射和中文题材标签，用东方财富妙想自选股和选股接口抓取 A 股盘中或最新交易日行情，按 `/themes` 权重计算题材加权涨跌幅，用中文题材名输出 TOP10 和 BOTTOM10，并对 TOP3 题材各选 1 只涨幅最高的代表股，用股吧线索和妙想资讯辅助判断题材为什么异动。该 skill 的特点是盘中可用，并且会实时报告抓取进度：自选接口覆盖多少、还需补抓多少、补抓批次完成到第几批、是否遇到限频重试、最终是否补齐。

依赖：必需 — 打包的 `/themes` 数据文件（`assets/themes/theme-data.json` 和 `assets/themes/theme-label-i18n.json`）、`mx-zixuan`、`mx-xuangu`；必需（TOP3 驱动检查）— `mx-search`、`cn-stock-move-reason`；可选 — `mx-data`（用于后续追查财务或估值）。

适用场景：

- 盘中查看打包 `/themes` A 股题材里哪些涨得最好、哪些最差。
- 先用东方财富自选股快速拿行情，再用妙想选股补齐自选接口没有返回的题材成分。
- 按题材权重输出 A 股题材强弱榜，而不是简单按板块名称或单只股票排序。
- 只在回答中显示完整 TOP10、BOTTOM10 和 TOP3 题材驱动检查，不默认写文件。

### [`stock-sentiment-analysis`](docs/skills/stock-sentiment-analysis.md)

给其他股票 skill 复用的情绪面分析框架，用于判断 A 股情绪周期、主线/跟随、预期差、论坛/掲示板温度、拥挤交易和跨市场 risk-on/risk-off。公开版不包含私人 RAG、`Stocks` 文件夹、个人标签或原始资料。

依赖：可选 — `cn-stock-move-reason`、`jp-stock-move-reason`、`stock-technical-analysis`、`us-stock-gamma-moomoo`（作为证据来源或协同分析）；`mx-data`、`mx-search`、`mx-xuangu`（A 股证据、题材成分和筛选增强）；`mx-zixuan`（仅用户明确要求自选股任务时）。

适用场景：

- 把股吧/掲示板热度、新闻预期差、板块广度和图形确认整合成情绪结论。
- 给 `cn-stock-move-reason`、`jp-stock-move-reason`、`stock-technical-analysis`、`us-stock-gamma-moomoo` 提供统一情绪框架。
- 在用户指定私有 RAG 目录时，可帮助用户建立本地索引，只记录主题、来源别名、页码/slide 范围、关键词和公开安全摘要；不把私有材料写入公开仓库。

### [`macro-news-check`](docs/skills/macro-news-check.md)

给其他市场 skill 调用的宏观快讯检查工具，只在个股、指数、技术分析或 gamma 分析确实需要当前宏观/大盘背景时使用。它优先查看金十，再用华尔街见闻和 FinancialJuice 补充交叉确认。

依赖：无。

适用场景：

- 判断个股或指数异动是否受利率、汇率、央行、经济数据、商品、地缘或大盘 risk-on/risk-off 影响。
- 给 `cn-stock-move-reason`、`jp-stock-move-reason`、`stock-technical-analysis`、`us-stock-gamma-moomoo` 提供宏观 tape。
- 把 2-5 条关键快讯转化为对当前标的的主因/放大器/背景噪音判断。

### [`market-daily-strategist`](docs/skills/market-daily-strategist.md)

面向美股、日股和 A 股的中文市场策略报告路由层，覆盖盘前策略、收盘复盘和单只长线推荐。它按用户意图读取对应市场和时段的 reference，并把宏观、异动原因、情绪周期、技术结构和可用的本地行情工具压缩进一份决策导向报告。

依赖：可选 — `macro-news-check`、`stock-sentiment-analysis`、`stock-technical-analysis`、`cn-stock-move-reason`、`jp-stock-move-reason`、`us-stock-gamma-moomoo`（按市场和问题协同分析）；`mx-data`、`mx-search`、`mx-xuangu`（A 股行情、资讯、板块/概念成分增强）；`mx-zixuan`（仅用户明确要求自选股任务时）。

适用场景：

- 写美股、日股或 A 股盘前策略。
- 写美股、日股或 A 股收盘复盘。
- 推荐一只美股、日股或 A 股/ETF/LOF，并给出买点、风险和验证条件。

### [`us-stock-gamma-moomoo`](docs/skills/us-stock-gamma-moomoo.md)

通过 moomoo OpenD 获取美股/美股期权数据，让 Codex 分析 gamma/GEX、gamma wall、gamma flip、SPX/SPY/ES 盘中结构，以及 0DTE 期权情景表。该 skill 需要本机运行 moomoo OpenD；如果环境不存在，应先引导安装或启动 OpenD。

依赖：无。环境要求：本机 moomoo OpenD。

适用场景：

- 分析普通美股或美股 ETF 的期权 gamma 结构。
- 分析 `.SPX`/SPXW 指数期权结构；如果拿不到指数实时行情或期权链，则用 SPY 期权、ES/CFD 或用户提供的指数锚进行换算并明确说明。
- 对 0DTE call/put 生成“时间 x 标的价位”的理论价值表，用于评估回本、止盈或止损点。
- 需要时生成本地 HTML gamma 报告；快速盘中问题可以只输出文字结论。

### [`stock-technical-analysis`](docs/skills/stock-technical-analysis.md)

针对美股、日股和 A 股做技术分析，重点看趋势结构、支撑压力、量价、KDJ/MACD/RSI、Vegas 通道、分时确认，以及“能不能到某个价位”的盘中判断。

依赖：可选 — `macro-news-check`、`stock-sentiment-analysis`、`cn-stock-move-reason`、`jp-stock-move-reason`、`us-stock-gamma-moomoo`（按标的和问题协同分析）；`mx-data`、`mx-search`、`mx-xuangu`（A 股行情、资讯、板块/概念成分和技术筛选增强）；`mx-zixuan`（仅用户明确要求自选股任务时）。

适用场景：

- 判断当前走势是强趋势延续、空中加油候选、回踩确认、冲高回落、高位分歧，还是破位反抽。
- 区分 touch、break、tradable hold，避免把一根影线误判为有效突破。
- 读取 moomoo/Yahoo/券商图表或截图，给出当前读数、技术结构、量价动能和下一验证点。
- 与日股/A股异动原因或美股 gamma skill 配合，判断催化是否被图形确认。

## 安装

把仓库 clone 到任意位置，然后把需要使用的 skill 目录复制或软链接到 `~/.codex/skills/`。

```bash
git clone https://github.com/tsetsugekka/codex-market-skills.git
mkdir -p ~/.codex/skills
ln -s /path/to/codex-market-skills/skills/market-calendar-google ~/.codex/skills/market-calendar-google
ln -s /path/to/codex-market-skills/skills/jp-stock-move-reason ~/.codex/skills/jp-stock-move-reason
ln -s /path/to/codex-market-skills/skills/cn-stock-move-reason ~/.codex/skills/cn-stock-move-reason
ln -s /path/to/codex-market-skills/skills/cn-theme-strength-mx ~/.codex/skills/cn-theme-strength-mx
ln -s /path/to/codex-market-skills/skills/stock-sentiment-analysis ~/.codex/skills/stock-sentiment-analysis
ln -s /path/to/codex-market-skills/skills/macro-news-check ~/.codex/skills/macro-news-check
ln -s /path/to/codex-market-skills/skills/market-daily-strategist ~/.codex/skills/market-daily-strategist
ln -s /path/to/codex-market-skills/skills/us-stock-gamma-moomoo ~/.codex/skills/us-stock-gamma-moomoo
ln -s /path/to/codex-market-skills/skills/stock-technical-analysis ~/.codex/skills/stock-technical-analysis
```

也可以只安装其中一个 skill。

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
用 /themes 的题材映射和 mx 抓一次 A 股题材强弱，显示 TOP10 和最差10。
```

```text
盘中看一下 A 股哪些题材涨得好，哪些题材最差。
```

```text
分析一下这只股票现在是主线启动、高潮分歧，还是退潮反抽。
```

```text
看一下金十、华尔街见闻和 FinancialJuice，现在有没有影响这个票的大盘或宏观消息。
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

## 安全说明

- `market-calendar-google` 会在用户明确要求时使用 Google Calendar 连接器创建或更新日历事件。
- `jp-stock-move-reason` 只读取公开网页/API，不读取 token，不写入外部服务，不调用 Gemini/OpenAI API。
- `cn-stock-move-reason` 只读取东方财富、搜狐证券等公开网页/API，不读取 token，不写入外部服务，不调用 Gemini/OpenAI API。
- `cn-theme-strength-mx` 必须使用东方财富妙想 `mx-zixuan` 和 `mx-xuangu`，并打包公开发布用的 `/themes` 快照；只在用户要求题材强弱/自选相关工作流时读取自选股，不自动添加、删除或修改自选股，不提交 `MX_APIKEY`、完整自选股列表、未经确认可公开发布的其他 `/themes` 派生数据、原始 API 响应或运行缓存。发布或更新该 skill 前，应从 DTM 工作目录的 `themes/public/` 刷新 `theme-data.json` 和 `theme-label-i18n.json`。
- `stock-sentiment-analysis` 只保存公开安全的通用情绪框架；不应提交私人 RAG、`Stocks` 文件夹、个人标签、原始笔记、截图或交易日志。
- `macro-news-check` 只读取公开宏观快讯页面/Feed/接口；不读取登录 cookie、token、账号数据或私有研究资料，不复制长篇新闻正文。
- `market-daily-strategist` 是报告路由和综合层；本地/私有行情工具只作为可选增强，不应把个人关注列表、私有输出或工具缓存提交到公开仓库。
- `us-stock-gamma-moomoo` 使用本机 moomoo OpenD 行情接口，不调用交易解锁接口；公开版不依赖本地 `Stocks` 文件夹，不应提交个人账号、OpenD 日志、截图、私有行情输出、原创策略名或私有人名/handle。
- `stock-technical-analysis` 只保存通用技术分析规则；公开版不依赖本地 `Stocks` 文件夹，不应提交个人仓位、交易计划、截图原图、私有研究路径、专有指标名、原创策略名或私有人名/handle。
- 不要把个人关注列表、凭据、API key、`.env`、`Stocks/`、私有 RAG、运行缓存或私有输出提交到本仓库。
- 面向 GitHub 用户的发布/隐私摘要见 [`docs/release-and-privacy.md`](docs/release-and-privacy.md)；Codex runtime 规则以 `shared/references/release-and-privacy.md` 为准。

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
  cn-theme-strength-mx/
    SKILL.md
    agents/openai.yaml
    assets/themes/theme-data.json
    assets/themes/theme-label-i18n.json
    scripts/refresh_theme_assets.py
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
  release-and-privacy.md
  skills/
    market-calendar-google.md
    jp-stock-move-reason.md
    cn-stock-move-reason.md
    cn-theme-strength-mx.md
    macro-news-check.md
    market-daily-strategist.md
    stock-sentiment-analysis.md
    us-stock-gamma-moomoo.md
    stock-technical-analysis.md
shared/
  references/release-and-privacy.md
```

## 语言

- 中文：`README.md`
- 日本語：`README.ja.md`
- English: `README.en.md`
