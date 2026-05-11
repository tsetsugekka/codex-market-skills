# Codex Market Skills

Codex Market Skills 是一组面向交易、投资研究和市场日程管理的 Codex skills。项目原先只包含 `market-calendar-google`，现在扩展为一个多 skill 仓库：同一个 GitHub 项目中保存多个边界清晰、可单独安装和维护的市场工作流。

## 当前包含的 skills

### [`market-calendar-google`](skills/market-calendar-google/README.md)

整理美股财报、日股财报、中美日宏观数据、央行事件、拍卖和其他重要财经事件，并按用户规则写入 Google Calendar。

适用场景：

- 整理本周或下周 Earnings Whispers 美股财报图。
- 根据关注列表筛选美股或日股财报。
- 整理中美日四星以上财经事件。
- 把事件按日本时间写入 Google Calendar，并避免重复。

### [`jp-stock-move-reason`](skills/jp-stock-move-reason/README.md)

针对用户输入的日本股票代码，抓取 Yahoo Finance 实时板、Yahoo 掲示板、Yahoo/Kabutan/Traders 新闻以及基础指标，让 Codex 分析个股异动理由。该 skill 不调用 Gemini 或其他 LLM API，也不读取任何凭据。

适用场景：

- 分析某只日股为什么急涨、急跌或突然放量。
- 区分新闻确认的催化和 Yahoo 掲示板上的市场思惑。
- 查看当前涨跌幅、市值、PER/PBR、信用倍率、掲示板温度等辅助信息。

### [`cn-stock-move-reason`](skills/cn-stock-move-reason/README.md)

针对用户输入的单只 A 股代码，抓取东方财富公开行情、公告、股吧/资讯帖，并结合搜狐指数/板块页面与 A 股涨跌家数背景，让 Codex 分析个股异动理由、是否大盘/板块/个股共振，以及短线情绪周期位置。该 skill 不调用 Gemini 或其他 LLM API，也不读取任何凭据。

适用场景：

- 分析某只 A 股为什么涨停、跌停、炸板或突然放量。
- 区分公告/业绩确认催化和股吧题材思惑。
- 结合大盘指数、行业/概念板块和涨跌家数，判断是市场共振、板块主线，还是个股独立催化。
- 按冰点、修复/潜伏、启动、加速、高潮、高位分歧/分化、退潮判断短线情绪阶段。

## 安装

把仓库 clone 到任意位置，然后把需要使用的 skill 目录复制或软链接到 `~/.codex/skills/`。

```bash
git clone https://github.com/tsetsugekka/codex-market-skills.git
mkdir -p ~/.codex/skills
ln -s /path/to/codex-market-skills/skills/market-calendar-google ~/.codex/skills/market-calendar-google
ln -s /path/to/codex-market-skills/skills/jp-stock-move-reason ~/.codex/skills/jp-stock-move-reason
ln -s /path/to/codex-market-skills/skills/cn-stock-move-reason ~/.codex/skills/cn-stock-move-reason
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

## 安全说明

- `market-calendar-google` 会在用户明确要求时使用 Google Calendar 连接器创建或更新日历事件。
- `jp-stock-move-reason` 只读取公开网页/API，不读取 token，不写入外部服务，不调用 Gemini/OpenAI API。
- `cn-stock-move-reason` 只读取东方财富、搜狐证券等公开网页/API，不读取 token，不写入外部服务，不调用 Gemini/OpenAI API。
- 不要把个人关注列表、凭据、`.env`、运行缓存或私有输出提交到本仓库。

## 仓库结构

```text
skills/
  market-calendar-google/
    SKILL.md
    README.md
    agents/openai.yaml
  jp-stock-move-reason/
    SKILL.md
    EXPERIENCE.md
    README.md
    scripts/stock_move_sources.py
  cn-stock-move-reason/
    SKILL.md
    EXPERIENCE.md
    README.md
    agents/openai.yaml
    scripts/stock_move_sources.py
```

## 语言

- 中文：`README.md`
- 日本語：`README.ja.md`
- English: `README.en.md`
