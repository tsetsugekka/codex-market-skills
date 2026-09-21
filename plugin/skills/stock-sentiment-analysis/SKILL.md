---
name: stock-sentiment-analysis
description: 从催化、预期差、市场宽度、领导股和价格反应分析市场情绪、拥挤度及主线周期。
---

# Stock Sentiment Analysis

## 跨环境执行

先按[环境能力路由](../market-daily-strategist/references/runtime-capabilities.md)发现当前会话已安装、已连接且有权限的 Skill、工具、网页和计算能力。OpenD/moomoo、妙想、同花顺等是可选数据能力；不能由 ChatGPT Web、工作环境或 Codex 的名称推定可用性。优先复用已取得且仍有效的资料。研究来源顺序、字段与计算方法不因环境不同而省略；缺能力时说明具体缺口，不宣称已采集或已计算。

此包按各 Skill 入口附带可移植 Python 脚本；可读取文件不等于能执行，能执行不等于能联网。先确认能力，再按环境路由选择随包脚本、可用扩展或公开网页；仅有用户资料时执行相同筛选与计算，无执行能力时按文字流程研究并标出未计算项。外部供应商采集器只在已安装且可用时调用。访问失败、限流与权限处理遵循当前工具及环境规则，不复制机器专用沙箱设置。实际加载所用的同包 Skill 和参考，不只在回答中提名字。

本插件用于研究，写日历、账户或交易需要对应授权。普通研究不自动访问私人自选或持仓，不修改自身、其他 Skill 或任务规则；自动任务保持自己的输出、归档和授权合同。用户指定的私人资料仅在本轮授权范围内使用，不写入插件。

Use this skill as the shared sentiment layer for market skills. It does not fetch data by itself; it tells Codex how to interpret evidence gathered by `cn-stock-move-reason`, `jp-stock-move-reason`, `stock-technical-analysis`, `us-stock-gamma-moomoo`, public news, forums, breadth, and user-provided screenshots or notes.

This public-safe skill must not contain personal information, API keys, account data, private paths, raw screenshots, full copied notes, ticker-specific personal trade logs, or proprietary labels from a private RAG corpus. It must remain usable without any private RAG folder.

## Reference Reading Rule

When this skill selects a reference file, first scan the file structure, then read the sections and nearby guardrails relevant to the current task. Read the complete file when it is short, when the task is broad or strategic, or when partial reading could miss constraints. Do not rely on stale memory or heading-only scans.

## Workflow

1. Read the relevant areas of [experience](references/experience.md) before deep analysis; read the full file when the task is broad or the active playbook may affect the answer.
2. During decomposition, actively expand stock, index, and theme questions into emotion-cycle, main-line/follower, expectation-gap, crowding, cross-market sentiment, or mainline/funds/game/cycle checks when these lenses can change the conclusion, even if the user did not explicitly request them. For collective sector surges, continuation questions, and market-sector-stock resonance, apply `Market-Sector-Stock Resonance And Continuation` from [sentiment-framework](../../../skills/stock-sentiment-analysis/references/sentiment-framework.md); separate logic durability, tape continuity, and entry quality instead of treating a strong narrative as an automatic buy point. Read the relevant areas of [sentiment-framework](../../../skills/stock-sentiment-analysis/references/sentiment-framework.md).
3. Gather or receive evidence from the market-specific skill first:
   - A-shares: prefer `cn-stock-move-reason` for quote, announcements, 股吧, board ranks, breadth, and A-share emotion cycle.
   - Japanese stocks: prefer `jp-stock-move-reason` for quote, news, Yahoo 掲示板, metrics, and theme/peer context.
   - US stocks/indexes: prefer `us-stock-move-reason` for why-up/why-down/mover questions, choose `us-stock-gamma-moomoo` for option/gamma questions, and choose `stock-technical-analysis` for chart/trend questions; use them together when catalyst, positioning, and price action all matter.
   - For U.S. community discussion evidence, `moomoo-comment-sentiment` can be used when installed. Treat it as a moomoo community sample that helps measure retail heat, disagreement, chasing, and panic; it is not a full-market sentiment survey and must not replace news, filings, earnings, option positioning, or price behavior.
   - Pre-screened narrative-status entries from market reports can be used as social-media-derived clues for current themes, mainline candidates, and crowding/expectation-gap questions. Account/source quality can be assumed acceptable for screening, but timeliness is mandatory: stale source/update times are background only, not current sentiment evidence.
4. For A-share evidence, optional 东方财富妙想 skills can supplement the market-specific workflow when installed. MX data is an evidence and screening layer, not a replacement for the existing know-how: still apply source hierarchy, emotion-cycle staging, main-line/follower judgment, expectation-gap analysis, forum/news psychology, breadth, sector rotation, macro, and technical confirmation when relevant. Use `mx-data` for quote/financial/fund-flow/sector data, `mx-search` for news/announcements/research/policy, and `mx-xuangu` for sector constituents, concept stocks, peer screens, and natural-language condition screens. For A-share questions such as `这个板块有哪些股票`, `相关股`, `概念股`, `龙头股`, `板块成分`, or `同题材还有谁`, try `mx-xuangu` first when available; then use `mx-data`/`mx-search` selectively to classify purity, heat, and catalysts. If 妙想 is unavailable, continue with public sources or state the limitation. You may briefly suggest installing/configuring 妙想 only when it would materially improve the exact request; never make it a dependency.
5. Do not use account-touching 妙想 skills automatically. Use `mx-zixuan` only when the user explicitly asks to query/add/delete/filter 东方财富 self-selected stocks; for `自选股里哪些符合条件`, first try `mx-xuangu` constrained to self-selected stocks, and if unsupported, combine `mx-zixuan` self-selected results with `mx-xuangu` screening locally. Use `mx-moni` only for explicit simulated-portfolio queries or simulated trades.
6. Classify the move through three lenses: `confirmed catalyst`, `emotion/positioning`, and `technical confirmation`. When resonance matters, finish the hierarchy `market -> sector/theme -> stock` and test broad-market support, turnover/liquidity, participation breadth, industry-chain diffusion, continuing fundamental validation, and lifecycle position. Do not let forum heat replace confirmed news.

## DTM Context

Prefer data already obtained by the upstream market-specific skill. When the relevant context is missing, use the canonical JSON interfaces in `https://daytrading.monster/api-docs/`: `https://daytrading.monster/api/themes` for cross-market theme members and completed-session participation/relative strength; `https://daytrading.monster/api/chinastock-anomaly` for A-share theme rotation, limit-up structure, and move reasons; and `https://daytrading.monster/api/24hfeed/x-monitor` for discussion within the returned eight-hour snapshot window. Read `themes[]` and `constituents[]`, including coverage and quote dates; do not infer live flows from daily returns or whole-market sentiment from an account sample. Parse the `text/plain` bodies as JSON. Fetch only the layers needed for the question, retaining the existing source hierarchy and interpretation rules.

## Output Style

When used directly, answer in Chinese unless the user asks otherwise. Use this compact structure when useful:

1. `情绪结论`: risk-on/risk-off, early-cycle/late-cycle, panic, rotation, or crowded long.
2. `证据`: confirmed news, forum/post heat, breadth, sector peers, option/gamma positioning, and chart behavior.
3. `周期位置`: A-share seven-stage cycle when relevant; otherwise describe low-vol accumulation, early breakout, acceleration, distribution, or de-risking.
4. `主线判断`: leader/follower/defensive alternative/old-leader rebound/noise.
5. `验证条件`: what confirms continuation.
6. `失效条件`: what shows emotion has turned.

Do not give direct trading instructions. Give conditional conclusions and clearly label uncertain forum narratives as `思惑` or `未确认`.
