# Codex Market Skills

Codex Market Skills 是一组面向交易、投资研究和市场日程管理的 Codex skills。项目原先只包含 `market-calendar-google`，现在扩展为一个多 skill 仓库：同一个 GitHub 项目中保存多个边界清晰、可单独安装和维护的市场工作流。

## 当前包含的 skills

### [`market-calendar-google`](docs/skills/market-calendar-google.md)

整理美股财报、日股财报、中美日宏观数据、央行事件、拍卖和其他重要财经事件，并按用户规则写入 Google Calendar。

适用场景：

- 整理本周或下周 Earnings Whispers 美股财报图。
- 根据关注列表筛选美股或日股财报。
- 整理中美日四星以上财经事件。
- 把事件按日本时间写入 Google Calendar，并避免重复。

### [`jp-stock-move-reason`](docs/skills/jp-stock-move-reason.md)

针对用户输入的日本股票代码，抓取 Yahoo Finance 实时板、Yahoo 掲示板、Yahoo/Kabutan/Traders 新闻以及基础指标，让 Codex 分析个股异动理由。该 skill 不调用 Gemini 或其他 LLM API，也不读取任何凭据。

适用场景：

- 分析某只日股为什么急涨、急跌或突然放量。
- 区分新闻确认的催化和 Yahoo 掲示板上的市场思惑。
- 查看当前涨跌幅、市值、PER/PBR、信用倍率、掲示板温度等辅助信息。

### [`cn-stock-move-reason`](docs/skills/cn-stock-move-reason.md)

针对用户输入的单只 A 股代码，抓取东方财富公开行情、公告、股吧/资讯帖，并结合搜狐指数/板块页面与 A 股涨跌家数背景，让 Codex 分析个股异动理由、是否大盘/板块/个股共振，以及短线情绪周期位置。该 skill 不调用 Gemini 或其他 LLM API，也不读取任何凭据。

适用场景：

- 分析某只 A 股为什么涨停、跌停、炸板或突然放量。
- 区分公告/业绩确认催化和股吧题材思惑。
- 结合大盘指数、行业/概念板块和涨跌家数，判断是市场共振、板块主线，还是个股独立催化。
- 按冰点、修复/潜伏、启动、加速、高潮、高位分歧/分化、退潮判断短线情绪阶段。

### [`stock-sentiment-analysis`](docs/skills/stock-sentiment-analysis.md)

给其他股票 skill 复用的情绪面分析框架，用于判断 A 股情绪周期、主线/跟随、预期差、论坛/掲示板温度、拥挤交易和跨市场 risk-on/risk-off。公开版不包含私人 RAG、`Stocks` 文件夹、个人标签或原始资料。

适用场景：

- 把股吧/掲示板热度、新闻预期差、板块广度和图形确认整合成情绪结论。
- 给 `cn-stock-move-reason`、`jp-stock-move-reason`、`stock-technical-analysis`、`us-stock-gamma-moomoo` 提供统一情绪框架。
- 在用户指定私有 RAG 目录时，可帮助用户建立本地索引，只记录主题、来源别名、页码/slide 范围、关键词和公开安全摘要；不把私有材料写入公开仓库。

### [`us-stock-gamma-moomoo`](docs/skills/us-stock-gamma-moomoo.md)

通过 moomoo OpenD 获取美股/美股期权数据，让 Codex 分析 gamma/GEX、gamma wall、gamma flip、SPX/SPY/ES 盘中结构，以及 0DTE 期权情景表。该 skill 需要本机运行 moomoo OpenD；如果环境不存在，应先引导安装或启动 OpenD。

适用场景：

- 分析普通美股或美股 ETF 的期权 gamma 结构。
- 分析 `.SPX`/SPXW 指数期权结构；如果拿不到指数实时行情或期权链，则用 SPY 期权、ES/CFD 或用户提供的指数锚进行换算并明确说明。
- 对 0DTE call/put 生成“时间 x 标的价位”的理论价值表，用于评估回本、止盈或止损点。
- 需要时生成本地 HTML gamma 报告；快速盘中问题可以只输出文字结论。

### [`stock-technical-analysis`](docs/skills/stock-technical-analysis.md)

针对美股、日股和 A 股做技术分析，重点看趋势结构、支撑压力、量价、KDJ/MACD/RSI、Vegas 通道、分时确认，以及“能不能到某个价位”的盘中判断。

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
ln -s /path/to/codex-market-skills/skills/stock-sentiment-analysis ~/.codex/skills/stock-sentiment-analysis
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
分析一下这只股票现在是主线启动、高潮分歧，还是退潮反抽。
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
- `stock-sentiment-analysis` 只保存公开安全的通用情绪框架；不应提交私人 RAG、`Stocks` 文件夹、个人标签、原始笔记、截图或交易日志。
- `us-stock-gamma-moomoo` 使用本机 moomoo OpenD 行情接口，不调用交易解锁接口；公开版不依赖本地 `Stocks` 文件夹，不应提交个人账号、OpenD 日志、截图、私有行情输出、原创策略名或私有人名/handle。
- `stock-technical-analysis` 只保存通用技术分析规则；公开版不依赖本地 `Stocks` 文件夹，不应提交个人仓位、交易计划、截图原图、私有研究路径、专有指标名、原创策略名或私有人名/handle。
- 本地安装目录里的 skill 可视为私密/本地工作版；本仓库里的 skill 是 GitHub 公开版。若本地同时存在公开版和私密版，本地分析可优先使用私密版；但上传 GitHub 或发布时必须使用本仓库公开版，并按 `stock-sentiment-analysis/references/release-and-privacy.md` 做检查。
- 更新成对的公开版/私密版时，公开安全的通用规则要同步到公开版；私有路径、私有标签、原始资料、截图、个人交易上下文只留在私密版或私有 RAG。
- 如果要结合个人学习资料，请在公开仓库外建立私有 RAG/知识库；它可以服务情绪面、技术分析、gamma/期权结构等多个 skill；只把抽象后的通用经验写回 skill，并删除私有路径、专有名词、账号信息和可识别个人信息。
- 不要把个人关注列表、凭据、API key、`.env`、`Stocks/`、私有 RAG、运行缓存或私有输出提交到本仓库。

## 仓库结构

```text
skills/
  market-calendar-google/
    SKILL.md
    agents/openai.yaml
  jp-stock-move-reason/
    SKILL.md
    references/experience.md
    scripts/stock_move_sources.py
  cn-stock-move-reason/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    scripts/stock_move_sources.py
  stock-sentiment-analysis/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    references/sentiment-framework.md
  us-stock-gamma-moomoo/
    SKILL.md
    references/
    scripts/gamma_report.py
    scripts/option_scenario_table.py
  stock-technical-analysis/
    SKILL.md
    agents/openai.yaml
    references/
docs/
  skills/
    market-calendar-google.md
    jp-stock-move-reason.md
    cn-stock-move-reason.md
    stock-sentiment-analysis.md
    us-stock-gamma-moomoo.md
    stock-technical-analysis.md
```

## 语言

- 中文：`README.md`
- 日本語：`README.ja.md`
- English: `README.en.md`
