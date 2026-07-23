# JP Stock Move Reason

`jp-stock-move-reason` 是一个用于 Codex 的日本股票异动解析 skill。它针对用户输入的日股代码，从 Yahoo Finance、Yahoo 掲示板、Yahoo/Kabutan/Traders 新闻和公开指标中收集证据，再由 Codex 归纳可能的上涨、下跌或放量原因。

skill 目录里的 `SKILL.md` 是给 Codex 执行时读取的规则文件；本文档是给 GitHub 用户阅读的公开说明。

## 能做什么

- 获取当前股价、涨跌幅、成交量等行情信息。
- 获取市值、PER、PBR、股息收益率、信用倍率等基础指标。
- 抓取 Yahoo 掲示板近期评论，用来观察散户关注点和市场温度。
- 汇总 Yahoo、Kabutan、Traders Web 等公开新闻线索。
- 检查机构评级当前页数据，确认目标代码是否有券商评级、目标价上调/下调、评级上调/下调或集中评级变化。实际只读取当前页公开 JSON：`/rating/data.json`、`/rating/quotes.json`、`/rating/reasons.json`。不读取 `/rating/days/*` 历史日档；只有有当前匹配评级/目标价变化并可能影响异动时才在正文提及，未匹配或无新变化时不写负面占位句。
- 财报或指引相关问题会额外查找公司 IR、TDnet/Kabutan PDF、決算説明資料、補足説明資料、事業計画及び成長可能性に関する事項、中期経営計画、決算説明会 Q&A、产品/项目发布等说明材料；不仅看财报数字和掲示板。
- 帮 Codex 区分“新闻确认的催化”和“掲示板上的思惑”。
- 按日本交易时段自动选择 Kabutan 普通涨跌榜、PTS day 或 PTS night，筛选有效异动后计算成交额 Top10，并逐只补充原因。

## 【依赖】

- 必需：无。基础异动解析由本 skill 自带脚本和公开网页/API 完成。

## 【协同调用】

- `stock-sentiment-analysis`：当掲示板/新闻线索涉及主题主线、跟随、拥挤、leader/follower、旧龙反抽、risk-on/risk-off 或预期差时协同分析。
- `macro-news-check`：当个股异动可能受 Nikkei/TOPIX、JPX 行业、日经期货、JGB、美元兑日元、BOJ/MOF、海外宏观、商品或地缘影响时协同确认。
- `stock-technical-analysis`：当价格行为涉及支撑压力、突破失败、趋势破坏、量价确认、盘中执行或催化是否被图形接受/否定时协同验证。

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
- `--comments 0`：完全跳过 Yahoo 掲示板请求，不只是把输出限制为0条。
- `--bulk-reason`：榜单批量原因模式；关闭所有Yahoo页面和个股PTS请求，只读取
  Kabutan/Traders等非Yahoo证据。
- `--news-limit 15`：最多收集的新闻条数。
- `--sources yahoo,kabutan,traders`：指定新闻来源。
- `--market-hint 東証G`：在市场分类已知时辅助 Traders Web URL 选择。

## 涨跌成交额 Top10 副 skill

涨跌榜排名工作流位于：

- 执行规则：`skills/jp-stock-move-reason/references/pts-turnover-ranking.md`
- 排名脚本：`skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py`

它用于处理“看看当前涨跌榜”“跑一下 PTS”“PTS 涨跌 Top10”“夜间 PTS
成交额榜”等请求。默认同时抓取上涨榜和下跌榜，并按以下规则执行。

### 时间与 URL 路由

`--session auto` 按日本时间选择 Kabutan section：

- 交易日 `09:00-11:30`、`12:30-15:30`：使用普通涨跌幅榜。
- 交易日 `08:00-09:00`、`11:30-12:30`、`15:30-17:00`：使用 PTS day section。
- 其他时段、周末和非交易日：使用 PTS night section。
- 脚本自动识别周末；日本交易所工作日休市时显式使用 `--session night`。

等价选择逻辑：

```text
if 非交易日:
    session = night
elif 09:00 <= JST < 11:30 or 12:30 <= JST < 15:30:
    session = regular
elif 08:00 <= JST < 09:00 or 11:30 <= JST < 12:30 or 15:30 <= JST < 17:00:
    session = day
else:
    session = night
```

所有边界按左闭右开处理：`11:30` 切到 PTS day，`12:30` 切回普通榜，
`15:30` 再切到 PTS day。判定必须使用 JST。

对应页面：

- 普通上涨：`https://kabutan.jp/warning/?mode=2_1`
- 普通下跌：`https://kabutan.jp/warning/?mode=2_2`
- PTS 日中上涨：`https://kabutan.jp/warning/pts_day_price_increase`
- PTS 日中下跌：`https://kabutan.jp/warning/pts_day_price_decrease`
- 夜间上涨：`https://kabutan.jp/warning/pts_night_price_increase`
- 夜间下跌：`https://kabutan.jp/warning/pts_night_price_decrease`

### 筛选与排名口径

默认先筛选：

```text
abs(涨跌幅) >= 1%
出来高 > 2,000
```

Kabutan 榜单不一定直接提供出来额，因此按当前数据源估算：

```text
普通榜成交额 = 当前价 * 出来高
PTS出来额 = PTS价格 * PTS出来高
```

最终按计算出的成交额降序取上涨、下跌各 Top10。`出来高`只作为 `> 2,000`
的资格条件，默认不能误作排名指标；只有用户明确要求“按出来高排序”时才改用
原始出来高。

最终输出使用固定标题：

```text
上涨 Top10（涨幅大于1%/成交量大于2000/成交额排序）
下跌 Top10（跌幅大于1%/成交量大于2000/成交额排序）
```

普通榜使用上述标题；PTS day/night 在标题前加 `PTS`。页面时间戳和计算口径
写在标题下方。

```bash
python3 skills/jp-stock-move-reason/scripts/pts_turnover_ranking.py \
  --session auto \
  --side both \
  --min-abs-pct 1 \
  --min-volume 2000 \
  --top 10 \
  --reason-commands
```

Kabutan 页面以涨跌幅排序，脚本使用每页 50 条并继续翻页，直到页面越过 1%
阈值，避免只看第一页漏掉成交额较大的股票。

### 抓取规则与规范

- 使用 Kabutan 当前普通榜或 PTS day/night warning 页面，并强制通过
  `shared_perpage=50` Cookie 读取每页 50 条；不把可能滞后的 `noscript`、SEO
  静态内容当作当前榜单。
- 请求带 cache-busting 时间参数，解析页面显示的 `YYYY年MM月DD日 HH:MM現在`
  并在结果中报告该时间；Kabutan 普通榜和 PTS 通常约有15分钟延迟，不能称为逐笔实时数据。
- 上涨榜按页面顺序抓取，直到最后一条低于 `+1%`；下跌榜抓取到最后一条高于
  `-1%`。空页立即停止，并设置最大页数防止异常循环。
- 完成涨跌幅范围采集后，才应用 `出来高 > 2,000`，再计算成交额并排序；
  不能按页面原顺序或原始出来高直接取 Top10。
- 普通榜涨跌率相对前一个正规交易时段收盘价。PTS day 和 night 的比较基准应按
  页面时段说明处理，输出时不要混淆。
- 对同一主机超过三次连续请求后加入适度随机等待，不并发轰炸 Kabutan、Yahoo
  或揭示板。出现 HTTP 限流、DNS、超时、连接重置或连续空结果时，报告具体错误，
  停止提高请求频率，并按权限规范重试或使用已缓存证据。
- 最终提交答案前刷新一次榜单；若原因采集期间排名变化，只补抓新入榜代码，
  已核对且原因未变化的代码复用本轮结果，不重新全量采集。

### 原因分析

最终榜单默认必须包含 `原因` 列，除非用户明确只要数字。普通股票统一使用
`stock_move_sources.py --bulk-reason` 顺序核对Kabutan/Traders新闻、公司披露和
评级；批量流程不得访问Yahoo行情、Yahoo新闻或Yahoo掲示板，也不重复抓个股PTS。
完成非Yahoo证据分析后，最多只允许对2只原因仍不明确的股票补抓掲示板，两次
Yahoo请求随机间隔2至4秒。遇到HTTP 403/429、Access Denied、连接重置或异常空页面
后，当前任务立即停止所有Yahoo请求，不得马上重试。脚本还会跨进程强制保持
Yahoo同主机请求随机间隔2至4秒；403/429或封控页面会触发共享的30分钟本地冷却，
榜单任务不得删除或绕过冷却。ETF/ETN根据跟踪指数或策略解释，低成交额异动明确
标为低置信度。

## 需要的权限和来源

- 只读取公开网页或公开 API。
- 不读取本地 token、Cookie、`.env` 或其他凭据。
- 不写入任何外部服务。
- 不调用 Gemini、OpenAI API 或其他 LLM API；分析由当前 Codex 会话完成。
- 评级 JSON 只作为当前公开评级/目标价线索；若目标代码未出现在当前数据中，不能推断全市场没有机构评级。正文默认不点名聚合站或页面名；用户要求来源时，可在单独 source 列表放 URL。
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
