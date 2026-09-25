---
name: stock-technical-analysis
description: 分析股票与指数的趋势、支撑压力、量价动能、突破回踩和有条件的入场止损退出计划。
---

# Stock Technical Analysis

## 跨环境执行

先按[环境能力路由](../market-daily-strategist/references/runtime-capabilities.md)发现当前会话已安装、已连接且有权限的 Skill、工具、网页和计算能力。OpenD/moomoo、妙想、同花顺等是可选数据能力；不能由 ChatGPT Web、工作环境或 Codex 的名称推定可用性。优先复用已取得且仍有效的资料。研究来源顺序、字段与计算方法不因环境不同而省略；缺能力时说明具体缺口，不宣称已采集或已计算。

此包按各 Skill 入口附带可移植 Python 脚本；可读取文件不等于能执行，能执行不等于能联网。先确认能力，再按环境路由选择随包脚本、可用扩展或公开网页；仅有用户资料时执行相同筛选与计算，无执行能力时按文字流程研究并标出未计算项。外部供应商采集器只在已安装且可用时调用。访问失败、限流与权限处理遵循当前工具及环境规则，不复制机器专用沙箱设置。实际加载所用的同包 Skill 和参考，不只在回答中提名字。

本插件用于研究，写日历、账户或交易需要对应授权。普通研究不自动访问私人自选或持仓，不修改自身、其他 Skill 或任务规则；自动任务保持自己的输出、归档和授权合同。用户指定的私人资料仅在本轮授权范围内使用，不写入插件。

Use this skill when the user asks about price action, technical setup, intraday odds, support/resistance, trend continuation, pullback risk, or chart-based timing for US stocks, Japanese stocks, or A-shares.

This public-safe skill is self-contained and contains only generalized technical-analysis methods. Do not commit personal information, API keys, account data, private RAG files, or private research materials to GitHub. It must not store personal positions, private research paths, proprietary indicator names, private person names/handles, or private strategy labels. It may use a user-specified private RAG folder during a session, but the skill must remain usable without it.

## Core Rule

Before deep analysis, read [experience](references/experience.md) if it exists, but only the `Active Playbook` sections unless the user explicitly asks for historical lessons. Apply those lessons to intraday execution realism, pressure/support confirmation, and post-discussion learning.

Cross-skill calls are operational. When this workflow says to use another market skill, actually load that skill's `SKILL.md` and required references when available in this package or environment. Do not merely mention the other skill by name in the answer.

When a live chart is visible in moomoo or another trading/chart app, use the chart directly if the user asks for `现在`, `再看看`, `moomoo`, `分时`, `图表`, `资金流`, `盘口`, or asks whether a level is being confirmed. Confirm the ticker and chart timeframe before reading signals.

For U.S. stocks and ETFs, prefer direct moomoo OpenD 1-minute K-line data over screenshot-only reads when OpenD is available. Subscribe to `SubType.K_1M` first, then call `get_cur_kline`; if the subscription fails because of missing permissions, unsupported symbols, or index restrictions, fall back to the moomoo app chart or a user-provided screenshot. OpenD may not support U.S. index K-lines such as `.SPX`, and some local setups may not have Japanese-stock or A-share permissions, so use SPY or the relevant ETF as a proxy only when appropriate and state the proxy clearly. When using SPY to judge SPX intraday structure, convert SPY levels into SPX levels before answering, using the freshest SPX or ES/SPX anchor available; report SPX levels first and note the SPY proxy only as source context.

For U.S. single-stock technical anomaly checks, use `moomoo-technical-anomaly` as an optional first-pass scanner when it is installed and OpenD is available. Treat its K-line, MA, MACD, RSI, KDJ, BOLL, and other abnormal-event output as a prompt for where to look, not as a buy/sell conclusion. The final technical judgment must still follow this skill's own framework: trend location, VWAP / moving-average relationship, volume-price confirmation, momentum divergence, support/resistance, failed breakout, and whether price holds after the signal.

Never answer only by following the latest tick. Use the sequence:

1. Identify the return thesis and holding horizon: crisis-beta, core-quality swing, dividend/income, event repricing, quality value, growth/optionality, or another clearly stated thesis. If the user only provides a chart, state that technical analysis can define execution invalidation but cannot prove a fundamental thesis.
2. Determine the timeframe: intraday trade, 1h+ swing, trend holding, or post-event reaction. For 1h+ and swing judgments, combine technicals with sentiment/news context instead of reading the chart alone.
3. Read price location: current price versus prior high/low, opening price, yesterday close, VWAP if available, 5/20-day lines, and obvious pressure/support.
4. Check volume-price confirmation: breakout must show volume and stand above the level; volume without price progress is possible distribution; shrinking pullback can be healthy only if support holds.
5. Check momentum: KDJ, MACD, RSI, and whether price makes a new high while momentum does not.
6. Check structure: trend continuation, high-level divergence, 空中加油, 回踩确认, 破位反抽, or 冲高回落.
7. For U.S.-listed stocks/ETFs only, optionally use ChartExchange dark-pool/off-exchange levels as hidden-liquidity reference zones when the stock has unusual volume, unexplained movement, repeated support/resistance, or a news reaction that price is accepting/rejecting. Do not apply this to A-shares or Japanese stocks. Dark-pool data has no buy/sell side; a level matters technically only after price confirms it with acceptance, rejection, repeated defense, or failure to reclaim.
8. Check market context: sector/peer confirmation, broad market tone, rates/FX/volatility when relevant, and for A-shares the emotion cycle. Call `macro-news-check` only when current macro or broad-market tape can plausibly change the read, such as index-wide selloffs/squeezes, rates/FX shocks, central-bank or data releases, commodities, geopolitics, or sudden futures moves. Use `stock-sentiment-analysis` for a deeper shared sentiment framework.
9. Give conditional conclusions and make entry, execution stop, thesis invalidation, time stop, and exit test the same return thesis.

For A-share technical reads, optionally use 东方财富妙想 skills when they are already installed, but keep them as a supplemental data layer rather than a replacement for the existing price-action workflow. Continue to judge trend, support/resistance, volume-price confirmation, sector/broad-market context, sentiment, and macro when relevant. `mx-data` can supplement current quote,涨跌幅,成交额/量,主力资金, historical prices, index/sector context, and valuation fields; `mx-search` can supplement current event/news context when a technical break may be news-driven; `mx-xuangu` can help build peer or board constituent comparisons and can run natural-language technical screens such as consecutive moving-average alignment plus price-above/below-MA conditions. If the user asks which A-shares belong to a sector/theme or asks for `相关股`, `概念股`, `龙头股`, or `板块成分`, use `mx-xuangu` first when available. Do not block the analysis if these skills are unavailable or fail; you may briefly suggest installing/configuring 妙想 only when that layer would materially improve the exact A-share request. Use `mx-zixuan` and `mx-moni` only when the user explicitly asks for self-selected-stock management/filtering or simulated portfolio/trade operations.

Do not read local research folders or indicator files by default. If the user explicitly provides a file or asks to learn from a specific document, extract only reusable public-safe rules. Do not store local file paths, proprietary indicator names, personal slogans, private strategy names, private person names/handles, or original document labels in this skill. Generic public concepts such as Vegas channels, KDJ, MACD, RSI, VWAP, and support/resistance may be retained.

## DTM Index And Theme Context

For DTM data, use the canonical JSON interfaces in `https://daytrading.monster/api-docs/`. When relevant to the target index, read `https://daytrading.monster/api/gamma/` for SPX/SPXW structure and SPX Camarilla, `https://daytrading.monster/api/range/nikkei` for Nikkei, or `https://daytrading.monster/api/range/sse` for Shanghai Composite. For the two index-trajectory endpoints, check `market_date`, `market_status` and `stale`; read fixed `camarilla` levels, `chart_range`, `daily_gaps`, `trajectory_5m`, and actually returned `moving_averages`/`vwap`. `price_trajectory.points` (`timestamp`, `index_value`) preserves all available session price points without interpolation or guaranteed tick completeness. Empty premarket trajectories must not be replaced with a prior session. These two endpoints contain no Gamma, GEX, DEX, expiry or options fields and do not replace individual-stock K-lines. HTML contracts: `https://daytrading.monster/api-docs/range-nikkei` and `https://daytrading.monster/api-docs/range-sse`. For theme context, select `https://daytrading.monster/api/themes?market=us`, `https://daytrading.monster/api/themes?market=jp`, or `https://daytrading.monster/api/themes?market=cn`; use members and completed-session performance, not assumed live intraday strength. Parse these `text/plain` bodies as JSON and reuse relevant data already obtained upstream.

## When To Load The Reference

For quick answers, apply the core rule directly.

For any of the following, read [technical-analysis-playbook](../../../skills/stock-technical-analysis/references/technical-analysis-playbook.md) first:

- The user asks "能不能到某个价格", "现在怎么看", "日内", "分时", "压力位", "支撑位", "技术分析", "买点", "卖点", "突破", "回踩", "空中加油", "KDJ", "MACD", "RSI", or "Vegas".
- The user asks for an entry plan, stop-loss, invalidation, holding period, take-profit, or exit plan.
- The stock has already moved sharply today.
- The answer may affect a same-day trading decision.
- You are using moomoo, Yahoo chart, or screenshots to read the chart.
- The user asks to use moomoo or another charting/trading app, or the chart is already visible and current.

For chart-app workflows, read the `Chart App Visual Workflow` section in [technical-analysis-playbook](../../../skills/stock-technical-analysis/references/technical-analysis-playbook.md).

For Japanese stocks and A-shares, prefer `jp-stock-move-reason` or `cn-stock-move-reason` as the first pass for news/emotion/catalyst context. Use this skill after that first pass when the user asks for chart timing, when the discussion becomes repeated/deeper, or when a 1h+ chart must confirm whether the narrative is accepted.

## Output Style

Reply in Chinese unless the user asks otherwise. Be decisive but conditional.

Use this compact structure when useful:

1. `结论`: state whether the setup is strong, weak, or only a candidate, and name the key confirmation level.
2. `技术结构`: trend, support/resistance, moving averages, and K-line pattern.
3. `量价/动能`: volume, KDJ/MACD/RSI, divergence, and funding/order-flow clues if available.
4. `触发条件`: what must happen for the bullish or bearish scenario to confirm.
5. `失效条件`: the level or signal that invalidates the read.
6. `计划一致性`: when a trade plan is requested, distinguish execution invalidation from thesis invalidation and state the exit/time-stop condition derived from the same thesis.

Avoid giving direct trading instructions. Use probability bands only when the evidence supports them, and explain what would change the probability.

## Coordination With Market Skills

This skill handles chart and technical structure. For catalysts, valuation, news, 掲示板/股吧, and move reasons, combine it with the relevant market skill:

- Japanese stocks: `jp-stock-move-reason`
- A-shares: `cn-stock-move-reason`
- Shared emotion framework: `stock-sentiment-analysis`
- Macro and broad-market tape when needed: `macro-news-check`
- US option gamma: `us-stock-gamma-moomoo`

For US stocks, choose based on the question: use `us-stock-gamma-moomoo` when option positioning, gamma walls, 0DTE, IV, or dealer hedging matter; use this skill when chart structure and timing matter; use both when an options map needs price-action confirmation.

When `moomoo-technical-anomaly` is available for a U.S. stock, it can be used before or alongside this skill to surface recent official technical anomaly events. Do not paste the anomaly output mechanically; translate it into this skill's structure and explicitly say whether price, volume, and levels confirm or reject the signal.

For U.S. dark-pool technical confirmation, use ChartExchange or FINRA-derived pages only as a secondary layer. Construct ChartExchange URLs from the actual listing venue and ticker, such as `nyse-anet`, `nasdaq-nvda`, or `nyse-spy`; SPY commonly resolves to `nyse-spy` on ChartExchange. If the listing venue is unknown, search the ticker first instead of reusing a prior URL. Treat high-volume dark-pool levels like unconfirmed support/resistance until price/VWAP/volume confirms them.

When both fundamentals/catalysts and technicals matter, gather source evidence first, then use this skill to judge whether the chart confirms, overextends, or contradicts the story.
