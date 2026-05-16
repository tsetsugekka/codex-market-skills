# JP Stock Move Reason

`jp-stock-move-reason` 是一个用于 Codex 的日本股票异动解析 skill。它针对用户输入的日股代码，从 Yahoo Finance、Yahoo 掲示板、Yahoo/Kabutan/Traders 新闻和公开指标中收集证据，再由 Codex 归纳可能的上涨、下跌或放量原因。

skill 目录里的 `SKILL.md` 是给 Codex 执行时读取的规则文件；本文档是给 GitHub 用户阅读的公开说明。

## 能做什么

- 获取当前股价、涨跌幅、成交量等行情信息。
- 获取市值、PER、PBR、股息收益率、信用倍率等基础指标。
- 抓取 Yahoo 掲示板近期评论，用来观察散户关注点和市场温度。
- 汇总 Yahoo、Kabutan、Traders Web 等公开新闻线索。
- 财报或指引相关问题会额外查找公司 IR、TDnet/Kabutan PDF、決算説明資料、補足説明資料、事業計画及び成長可能性に関する事項、中期経営計画、決算説明会 Q&A、产品/项目发布等说明材料；不仅看财报数字和掲示板。
- 帮 Codex 区分“新闻确认的催化”和“掲示板上的思惑”。

## 典型请求

```text
分析一下 6758 今天异动原因。
```

```text
看一下 6217 是新闻驱动还是掲示板思惑。
```

```text
用 jp-stock-move-reason 分析 7203 的下跌理由。
```

## 脚本用法

在仓库根目录运行：

```bash
python3 skills/jp-stock-move-reason/scripts/stock_move_sources.py 6758 --format markdown
```

常用参数：

- `--hours 24`：新闻和评论时间窗口。
- `--comments 30`：最多收集的 Yahoo 掲示板评论数。
- `--news-limit 15`：最多收集的新闻条数。
- `--sources yahoo,kabutan,traders`：指定新闻来源。
- `--market-hint 東証G`：在市场分类已知时辅助 Traders Web URL 选择。

## 需要的权限和来源

- 只读取公开网页或公开 API。
- 不读取本地 token、Cookie、`.env` 或其他凭据。
- 不写入任何外部服务。
- 不调用 Gemini、OpenAI API 或其他 LLM API；分析由当前 Codex 会话完成。
- 如果脚本在 Codex 沙箱中出现 `nodename nor servname provided`、`urlopen error` 或 Yahoo/Kabutan/Traders 连续空结果，应视为沙箱/DNS 网络失败，按正常审批流程提升网络权限后重跑；不能把沙箱空结果直接当成“没有新闻/没有掲示板讨论”。

## 经验模块

`skills/jp-stock-move-reason/references/experience.md` 用来保存可复用的分析经验，例如财报反应、预期差、估值和掲示板情绪的判断规则。Codex 默认只读取其中的 `Active Playbook`、`Compression Protocol` 和 `Conversation Learning Protocol`，避免历史经验越来越长后拖慢每次分析。

如果用户围绕同一只股票连续追加信息、质疑前次判断或讨论遗漏点，Codex 会在必要时把暴露出的可复用分析失误自动总结进经验模块。适用于 A 股和日股的经验会同步更新两边；只适合日股市场结构或数据源的经验才只写入本目录。一次性的股票事实和未经证实的思惑不应写入经验模块。

这个文件可以公开提交，但只应记录抽象后的经验规则。不要写入个人仓位、关注列表、私有研究笔记、凭据、Cookie 或原始长输出。

## 输出风格

Codex 会基于脚本输出，用中文写出类似短新闻长度的解释。一般包括最有力理由、补助理由、掲示板温度、确定度和注意点。若证据不足，会明确标注为思惑、期待、传闻或确认待ち。

## 公开安全说明

这个 skill 和脚本可以放在公开仓库中。请不要提交个人关注列表、私有分析输出、运行缓存、`.env`、token 或任何含有登录信息的文件。

本 skill 输出仅用于个人研究，不构成投资建议。掲示板评论尤其只代表公开社区发言，不能当作事实依据。
