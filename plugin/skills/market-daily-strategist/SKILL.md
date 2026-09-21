---
name: market-daily-strategist
description: 综合中国、日本和美国市场的盘前、盘中、收盘及长线研究，形成基于证据的条件策略。
---

# Market Daily Strategist

## 跨环境执行

先按[环境能力路由](../market-daily-strategist/references/runtime-capabilities.md)发现当前会话已安装、已连接且有权限的 Skill、工具、网页和计算能力。OpenD/moomoo、妙想、同花顺等是可选数据能力；不能由 ChatGPT Web、工作环境或 Codex 的名称推定可用性。优先复用已取得且仍有效的资料。研究来源顺序、字段与计算方法不因环境不同而省略；缺能力时说明具体缺口，不宣称已采集或已计算。

此包按各 Skill 入口附带可移植 Python 脚本；可读取文件不等于能执行，能执行不等于能联网。先确认能力，再按环境路由选择随包脚本、可用扩展或公开网页；仅有用户资料时执行相同筛选与计算，无执行能力时按文字流程研究并标出未计算项。外部供应商采集器只在已安装且可用时调用。访问失败、限流与权限处理遵循当前工具及环境规则，不复制机器专用沙箱设置。实际加载所用的同包 Skill 和参考，不只在回答中提名字。

本插件用于研究，写日历、账户或交易需要对应授权。普通研究不自动访问私人自选或持仓，不修改自身、其他 Skill 或任务规则；自动任务保持自己的输出、归档和授权合同。用户指定的私人资料仅在本轮授权范围内使用，不写入插件。

Use this skill for the user's market reports. This is not a scheduler; ignore any clock-trigger wording from the original prompts. Route by user intent:

- 美股盘前、开盘前、pre-market、盘前策略、美股今晚怎么做、美股明天如何做、今天美股怎么看、纳指今晚怎么看、标普明天怎么看、美国市场怎么做、美股大盘策略: read [us-pre-market](references/us-pre-market.md).
- 美股收盘、昨晚美股、复盘、close recap: read [us-close-briefing](references/us-close-briefing.md).
- 日股盘前、日经盘前、日本开盘前、明天日股如何做、今天日股怎么做、日经明天怎么看、日本市场怎么做、日股大盘策略: read [jp-pre-market](references/jp-pre-market.md).
- 日股收盘、今天日股复盘、日本市场复盘: read [jp-close-briefing](references/jp-close-briefing.md).
- A股盘前、A股早盘、开盘前策略、明天A股如何做、今天A股怎么做、A股明天怎么操作、大盘今天怎么办、沪指明天怎么看、创业板明天怎么看、科创板今天怎么做、A股大盘策略: read [cn-pre-market](references/cn-pre-market.md).
- A股收盘、A股复盘、今天A股市场回顾: read [cn-close-briefing](references/cn-close-briefing.md).
- 美股长线推荐、每日美股荐股、推荐一只美股: read [us-long-term](references/us-long-term.md).
- 日股长线推荐、每日日股荐股、推荐一只日股: read [jp-long-term](references/jp-long-term.md).
- A股长线推荐、每日A股荐股、推荐一只A股/ETF/LOF: read [cn-long-term](references/cn-long-term.md).

If the user asks a broad current-session or next-session question such as `明天/今天/今晚 + 市场/大盘/美股/纳指/标普/日股/日经/TOPIX/A股/沪指/创业板/科创板 + 如何做/怎么做/怎么看/怎么操作/怎么办`, treat it as a pre-market, current-session, or next-session strategy request for the named market, not as a generic macro question. If the market is named by an index, map it to the corresponding market reference above. If the user says only `盘前信息`, `收盘复盘`, `大盘怎么做`, or `推荐一只股票`, infer the market from the conversation. If unclear, ask one concise question for the market: 美股、日股、还是A股.

Always read [shared](references/shared.md) first, then only the one task-specific reference that matches the user request.

For any daily or one-name recommendation, also read [strategy-archetypes](../../../skills/market-daily-strategist/references/strategy-archetypes.md). Assign one primary strategy archetype before choosing entry, invalidation/stop, holding period, and exit. Do not combine an event-trade entry with a value-investing stop, or a swing entry with an indefinite long-term exit.

Reference reading rule: when this skill selects a reference file, first scan the file structure, then read the sections and nearby guardrails relevant to the current task. Read the complete file when it is short, when the task is broad or strategic, or when partial reading could miss constraints. Do not rely on stale memory or heading-only scans.

During question decomposition, actively expand broad market, sector, theme, and long-term stock questions into `mainline x funds x game x cycle` when that lens can change the conclusion, even if the user did not explicitly ask for it. In those cases, read the relevant sections of [global-mainline-funds-game-cycle](../../../skills/market-daily-strategist/references/global-mainline-funds-game-cycle.md). When the conclusion depends on whether a collective sector/theme surge can continue, load `stock-sentiment-analysis` and apply its market-sector-stock resonance framework across A-shares, U.S. stocks, or Japanese stocks.

## Core Workflow

1. Identify the report type and market.
2. Confirm current date/time in Japan time and whether the relevant next or current session is open. If the market is closed, follow the task-specific closed-market rule instead of forcing a normal report.
3. Gather latest data from reliable live sources. Use market-specific primary sources listed in the task reference.
4. For U.S. and Japan market reports, treat the current DayTrading.monster news-details index as the most important public theme-discovery source before synthesis. Use its linked news details and the X account monitor when they materially fit the question. These layers guide what to verify; they do not replace live market news, price/sector confirmation, filings, or official disclosures. Follow the DTM API routing in [shared](references/shared.md), including unfiltered Themes for cross-market transmission; this skill does not request the two DTM ratings APIs.
5. 通过当前可用网页/连接读取新闻索引，按市场与类别预筛；Python 与联网可用时，也可使用随包的 [narrative_status.py](../../../skills/market-daily-strategist/scripts/narrative_status.py)，从本 Skill 目录运行 `python3 scripts/narrative_status.py --market us --format json`（按需更换市场）。The source is `https://daytrading.monster/api/24hfeed/details`, grouping news titles, URLs and times by category. Account quality is assumed acceptable for screening; check API `generated_at`/`reviewed_at` and each entry's `time` against the report window. If it returns `stale_feed`, errors, or stale entries, skip or downgrade that layer rather than forcing it into the report. Open relevant detail URLs for the news content; the index has no direction or full narrative fields. Verify decisive items with live news, original/source reporting when available, and prices. Do not fetch historical/archive feeds or use static SEO text as current evidence.
   Use `https://daytrading.monster/api/24hfeed/x-monitor` for raw X context, checking its explicit eight-hour snapshot window. Treat this as social-media-derived source context, not verified news.
   For overall Japan PTS rising-mover discovery, prefer the three documented model APIs routed in [shared](references/shared.md); inspect the relevant session's `source_updated_at` before citing movers.
   For broad macro price context, DayTrading.monster home (`https://daytrading.monster/`) is useful for discovering TradingView symbols and whether a symbol is `D`, `24h`, or `365d`, but the latest widget prices and runtime news state are not visible in plain HTML/noscript fetches. Use a rendered browser/widget view or a programmatic TradingView/scanner equivalent before citing live prices from that dashboard.
   In the final report prose, do not name DayTrading.monster, 24H Feed, dashboard/widget names, page names, or other aggregator/source names by default. Describe the evidence generically as `当前叙事预筛`, `当前价格代理`, `PTS异动`, `评级线索`, or `行情确认`. Cite material claims with the actual source URL and time; source names need not dominate the prose.
6. Never invent prices, index levels, futures, percentage moves, gamma/options levels, flows, valuation, financials, or news. If unavailable, say `暂无具体数值` or `初步`.
7. Apply `shared.md` market-news and local-data discipline: scan enough current news before finalizing, avoid broad local-data sweeps, and prioritize items confirmed by price action, volume, flows, earnings, ratings, policy catalysts, or direct trading relevance.
8. Use simplified Chinese unless requested otherwise; use the task reference report structure, honoring the current user or Task format.

## Supporting Skills

This skill is a report router and synthesis layer. Use other market skills when they materially improve the report, but keep calls selective.

- Use `macro-news-check` when the report depends on current macro tape: rates, FX, oil, gold, commodities, central banks, economic data, geopolitics, broad risk sentiment, or live futures confirmation.
- For U.S. reports, use official moomoo skills as selective evidence helpers when installed: `moomoo-news-search` and `moomoo-stock-digest` for timely company/news context, `moomoo-comment-sentiment` for community heat, `moomoo-capital-anomaly` for capital-flow anomalies, `moomoo-derivatives-anomaly` for U.S.-applicable option anomaly dimensions, and `moomoo-technical-anomaly` for a first-pass technical anomaly scan. These are data and anomaly layers; keep this skill responsible for strategy synthesis.
- Use `us-stock-move-reason` for 1-3 important U.S. movers when the catalyst, earnings/guidance acceptance, news interpretation, option/flow anomaly, or community reaction needs a dedicated move-reason pass.
- Use `us-stock-gamma-moomoo` for US index/ETF option structure when SPX/SPY/QQQ/NQ gamma, GEX, 0DTE, dealer positioning, option walls, or intraday conversion levels could change the strategy.
- Use `stock-technical-analysis` for selected index/ETF/stock levels when the answer needs support/resistance, trend confirmation, intraday execution timing, breakout/pullback validation, or stop levels.
- Use `jp-stock-move-reason` or `cn-stock-move-reason` for 1-3 genuinely important Japanese/A-share movers when the catalyst is unclear or the stock drives the day's theme. Do not run move-reason analysis on every mover.
- Use `stock-sentiment-analysis` when crowding, leader/follower status, emotion cycle, old-leader rebound, theme acceptance/rejection, market-sector-stock resonance, or post-surge continuation affects the trading conclusion. Apply the six-factor matrix—broad-market support, turnover/liquidity, participation breadth, industry-chain diffusion, continuing fundamental validation, and non-terminal lifecycle—then separate logic durability, tape continuity, and entry quality.
- Use the narrative-status helper only as a theme-discovery and sentiment pre-screen. It can suggest which narratives to test, but it must not replace macro-news confirmation, market prices, filings/news, PTS/pre-market movers, sector breadth, gamma/options checks, or technical confirmation.
- Use 东方财富妙想 skills for A-share reports and sector questions when available, as supplemental data/search/screening only. They do not replace the report's existing market-news discipline, price-confirmed catalyst checks, emotion-cycle and leader/follower judgment, macro/technical confirmation, or source hierarchy. Use `mx-data` for quote, valuation, fund-flow, financials, index/sector data; `mx-search` for timely news, announcements, research, policy, and event explanations; `mx-xuangu` for sector/concept constituents, related-stock lists, condition screens, and peer comparisons. For questions like `A股某板块有哪些股票`, `相关股`, `概念股`, `龙头股`, or `板块成分`, try `mx-xuangu` first when available. Use `mx-zixuan` only when the user explicitly asks about 东方财富 self-selected stocks, and `mx-moni` only for explicit simulated-trading tasks.

Cross-skill calls are operational: actually load the supporting skill's `SKILL.md` and required references when using it. Keep supporting-skill output compressed into the final report instead of pasting separate mini-reports.

## Style

- Professional, concise, strategy-first.
- Start with a concise conclusion; task-reference titles are examples, not a universal length requirement.
- Prioritize actionable conclusions: 追高、等回踩、低吸、减仓、观察、避开财报风险、仓位与止损.
- Attribute important live figures and news to sources.
- When internal/current-page helper data is used, do not name DayTrading.monster, 24H Feed, dashboard/widget names, page names, or other aggregator/source names in the report prose by default; source URLs may appear in a separate source list when needed.
- For recommendation reports, clearly state that the output is not financial advice.

## Guardrails

- Read the public `/api/themes` for cross-market research; inspecting or modifying the DTM Themes project itself requires an explicit project task.
- For long-term recommendation reports, follow the requested count; for a one-name request select one target and avoid recently recommended names when that history is available in the conversation, logs, or user-provided context.
- For executable entry plans compare with the latest price, slippage and trading window; distinguish a current entry from a conditional pullback order. Apply a fixed distance cap only when requested.
