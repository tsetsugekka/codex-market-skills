# JP Stock Move Reason

`jp-stock-move-reason` 是一个用于 Codex 的日本股票异动解析 skill。它针对用户输入的日股代码，从 Yahoo Finance、Yahoo 掲示板、Yahoo/Kabutan/Traders 新闻和公开指标中收集证据，再由 Codex 归纳可能的上涨、下跌或放量原因。

这个目录里的 `SKILL.md` 是给 Codex 执行时读取的规则文件；本 `README.md` 是给 GitHub 用户阅读的公开说明。

## 能做什么

- 获取当前股价、涨跌幅、成交量等行情信息。
- 获取市值、PER、PBR、股息收益率、信用倍率等基础指标。
- 抓取 Yahoo 掲示板近期评论，用来观察散户关注点和市场温度。
- 汇总 Yahoo、Kabutan、Traders Web 等公开新闻线索。
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

## 输出风格

Codex 会基于脚本输出，用中文写出类似短新闻长度的解释。一般包括最有力理由、补助理由、掲示板温度、确定度和注意点。若证据不足，会明确标注为思惑、期待、传闻或确认待ち。

## 公开安全说明

这个 skill 和脚本可以放在公开仓库中。请不要提交个人关注列表、私有分析输出、运行缓存、`.env`、token 或任何含有登录信息的文件。

本 skill 输出仅用于个人研究，不构成投资建议。掲示板评论尤其只代表公开社区发言，不能当作事实依据。
