---
name: us-stock-move-reason
description: 分析美股和ETF异动，核验财报指引、公司事件、行业联动及期权或情绪背景。
---

# US Stock Move Reason

## 跨环境执行

先按[环境能力路由](../market-daily-strategist/references/runtime-capabilities.md)发现当前会话已安装、已连接且有权限的 Skill、工具、网页和计算能力。OpenD/moomoo、妙想、同花顺等是可选数据能力；不能由 ChatGPT Web、工作环境或 Codex 的名称推定可用性。优先复用已取得且仍有效的资料。研究来源顺序、字段与计算方法不因环境不同而省略；缺能力时说明具体缺口，不宣称已采集或已计算。

此包按各 Skill 入口附带可移植 Python 脚本；可读取文件不等于能执行，能执行不等于能联网。先确认能力，再按环境路由选择随包脚本、可用扩展或公开网页；仅有用户资料时执行相同筛选与计算，无执行能力时按文字流程研究并标出未计算项。外部供应商采集器只在已安装且可用时调用。访问失败、限流与权限处理遵循当前工具及环境规则，不复制机器专用沙箱设置。实际加载所用的同包 Skill 和参考，不只在回答中提名字。

本插件用于研究，写日历、账户或交易需要对应授权。普通研究不自动访问私人自选或持仓，不修改自身、其他 Skill 或任务规则；自动任务保持自己的输出、归档和授权合同。用户指定的私人资料仅在本轮授权范围内使用，不写入插件。

Use this skill as the U.S. stock counterpart to `jp-stock-move-reason` and `cn-stock-move-reason`. It is an evidence-gathering and synthesis workflow, not a trading bot.

This public-safe skill must not store account data, OpenD logs, API keys, cookies, private RAG paths, personal positions, screenshots, raw private notes, or proprietary labels. It may call official moomoo skills when installed, but those skills remain external data/anomaly providers.

## DTM API Context

Use the canonical JSON interfaces in `https://daytrading.monster/api-docs/` for DTM reads. `https://daytrading.monster/api/ratings-us` supplies recent analyst reports (US-local today and the preceding three calendar days); match the target symbol and report date. Use `https://daytrading.monster/api/themes` without a market filter to trace cross-market industry-chain and theme transmission across US, Japan, and China. Read `themes[]` and `constituents[]` for members, `weight`, `reason_zh`, coverage, and completed-session returns; check dates instead of treating them as live moves. Parse the `text/plain` response bodies as JSON.

## Workflow

1. Normalize the target into a U.S. market symbol such as `US.NVDA`, `US.DELL`, `US.SPY`, or `US.TSLA`. If the user gives only a name and the listing is ambiguous, ask one concise question. Treat broad index questions (`SPX`, `SPY`, `QQQ`, `NQ`) as U.S. index/ETF workflows and consider `macro-news-check` by default.

2. Establish whether the move is real:
   - Use `moomooapi` when available for snapshot, premarket/after-hours fields, daily or 1-minute K-line context, volume, turnover, market state, and basic stock information.
   - If OpenD or permissions fail, use public quote sources only as fallback and state the limitation.
   - For SPX, moomoo may reject `US..SPX` index snapshots while still allowing SPX/SPXW option chains. Use `SPY`, ES/CFD, or user-provided SPX anchors when needed and state the anchor.

3. Gather confirmed catalysts first:
   - Use `moomoo-news-search` or `moomoo-stock-digest` for current company news, earnings, guidance, ratings, orders, regulatory events, M&A, capital actions, analyst notes, and sector read-through.
   - When earnings are involved, apply expectation gap explicitly: `prior market expectation` -> `actual result / guidance / commentary` -> `above expectation`, `in line or merely landed`, or `below expectation`.
   - Do not let social posts, option prints, or technical signals replace confirmed filings/news.

4. Scan official moomoo anomaly layers when they are installed and relevant:
   - `moomoo-capital-anomaly`: use for capital-flow, broker, short-sale, or funds-flow anomaly requests. A `无异常` response is a usable result.
   - `moomoo-derivatives-anomaly`: use for U.S.-applicable option dimensions only: `option_unusual`, `option_volatility`, `option_volume_price`, `option_sentiment`, and `option_comprehensive`. Do not request Hong Kong warrant / CBBC dimensions for U.S. stocks. If a full scan returns an opaque backend error, retry with explicit U.S. option dimensions before concluding the skill is unavailable.
   - `moomoo-technical-anomaly`: use as a first-pass technical anomaly scanner, then verify with `stock-technical-analysis`.
   - `moomoo-comment-sentiment`: use for moomoo community heat, disagreement, chasing, panic, and representative viewpoints. Label it as a moomoo community sample, not a full-market sentiment survey.

5. Add supporting skills based on what the evidence shows:
   - Use `us-stock-gamma-moomoo` when options positioning, gamma walls, 0DTE, IV, SPX/SPY/QQQ, or dealer hedging can change the interpretation.
   - Use `stock-technical-analysis` when support/resistance, trend confirmation, failed breakout, VWAP, 1-minute K-lines, or intraday timing matter.
   - Use `stock-sentiment-analysis` when crowding, leader/follower status, risk-on/risk-off psychology, expectation reset, or social/community emotion changes the conclusion.
   - Use `macro-news-check` when Fed, rates, yields, USD, oil/gold, index futures, economic data, geopolitics, or broad market tape may be the main driver or amplifier.

6. Evidence priority:
   - Confirmed company news, filings, earnings, guidance, ratings, and direct disclosures.
   - Current quote, volume, gap, market state, and price acceptance/rejection.
   - Sector/peer and broad market context.
   - Option, capital-flow, short, and technical anomaly scans.
   - Community sentiment and social posts as secondary psychology evidence only.

## Output Style

Reply in Chinese unless the user asks otherwise. For every stock analyzed, use these six numbered sections in this exact order:

1. `最有力理由`: the most likely catalyst, source type, and expectation gap.
2. `补助理由`: sector/peer, macro, positioning, valuation, short/flow, or liquidity drivers.
3. `期权/资金/技术异动`: summarize only relevant moomoo anomaly and gamma/technical evidence; say `无异常` when a checked layer returns no anomaly.
4. `社区情绪`: moomoo community or other forum/social heat, representative views, and sample limitations.
5. `确定度`: high / medium / low, with one sentence explaining why.
6. `注意点`: what is unconfirmed, what could invalidate the read, and what needs a fresh check.

When evidence is thin, say so. Use `思惑`, `未确认`, or `确认待ち` for claims that appear only in community posts or option-flow interpretation. Do not give direct trading instructions; give conditional conclusions and validation levels when useful.

If supporting skills materially affect the conclusion, end with a compact `融合口径` line, for example:

```text
融合口径：moomoo news/digest + moomoo option/capital/technical anomaly + us-stock-gamma-moomoo gamma + stock-technical-analysis price action + macro-news-check tape.
```
