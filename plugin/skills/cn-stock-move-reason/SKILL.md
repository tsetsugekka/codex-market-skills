---
name: cn-stock-move-reason
description: 分析A股个股大涨、大跌、涨跌停、炸板及异常波动的原因，结合具体量价、公告、题材和预期差。
---

# CN Stock Move Reason

## 跨环境执行

先按[环境能力路由](../market-daily-strategist/references/runtime-capabilities.md)发现当前会话已安装、已连接且有权限的 Skill、工具、网页和计算能力。OpenD/moomoo、妙想、同花顺等是可选数据能力；不能由 ChatGPT Web、工作环境或 Codex 的名称推定可用性。优先复用已取得且仍有效的资料。研究来源顺序、字段与计算方法不因环境不同而省略；缺能力时说明具体缺口，不宣称已采集或已计算。

此包按各 Skill 入口附带可移植 Python 脚本；可读取文件不等于能执行，能执行不等于能联网。先确认能力，再按环境路由选择随包脚本、可用扩展或公开网页；仅有用户资料时执行相同筛选与计算，无执行能力时按文字流程研究并标出未计算项。外部供应商采集器只在已安装且可用时调用。访问失败、限流与权限处理遵循当前工具及环境规则，不复制机器专用沙箱设置。实际加载所用的同包 Skill 和参考，不只在回答中提名字。

本插件用于研究，写日历、账户或交易需要对应授权。普通研究不自动访问私人自选或持仓，不修改自身、其他 Skill 或任务规则；自动任务保持自己的输出、归档和授权合同。用户指定的私人资料仅在本轮授权范围内使用，不写入插件。

Use this skill to explain current single-stock moves from source evidence.

The skill accepts one stock at a time. It may also collect broad market context (indexes, sector/concept boards, and advance/decline counts) to judge whether the move is market-wide, sector-led, or stock-specific.

## Workflow

1. Read [experience](references/experience.md) before analysis, but only the `Active Playbook` sections unless the user explicitly asks for historical lessons. Apply those lessons when judging catalysts, sector共振, 股吧 emotion, A-share emotion-cycle position, and the stock's place in the market structure: 主线、助攻、补涨、防御、老龙反抽, or noise. When the request needs a deeper or reusable sentiment framework, also use `stock-sentiment-analysis` and its `references/sentiment-framework.md`.

   Cross-skill calls are operational. When this workflow says to use another market skill, actually load that skill's `SKILL.md` and required references when available in this package or environment. Do not merely mention the other skill by name in the answer.

   Required coordination: for A-share analysis, use this skill as the evidence-gathering entry point, and add supporting skills based on clues found during analysis, not only on the user's wording. 股吧 itself is an evidence source, not an automatic trigger for sentiment analysis. If 股吧/资讯/news reveals a concrete clue about main-line status, crowding, attack/defense rotation, leader/follower position, or emotion-cycle phase, load `stock-sentiment-analysis` to test that clue. If 股吧/资讯/news discusses the broad market, index pressure, policy/liquidity, FX/rates, commodities, overseas markets, or geopolitical drivers, load `macro-news-check` to verify the tape instead of accepting forum claims. If 股吧/资讯/news or the price move points to support/resistance, failed breakout, trend damage, or catalyst acceptance/rejection, load `stock-technical-analysis` to verify the chart. When the original question is directly about an index/broad tape such as 上证、深成指、创业板、科创50、A50、恒生科技/港股 spillover, load `macro-news-check` by default.

   Mandatory execution gate:
   - If the answer uses **宏观** or **快讯** to explain the stock, sector, index, liquidity, policy, FX/rates, commodities, overseas spillover, or geopolitics, load `macro-news-check`. Do not replace this layer with ad hoc web search.
   - If the answer uses **技术面** such as support/resistance, trend confirmation, failed breakout, volume-price behavior, intraday timing, or "能不能上/下", load `stock-technical-analysis`.
   - If the answer uses **情绪面** such as main-line status, crowding, emotion cycle, leader/follower, risk-on/risk-off, expectation gap, or forum psychology, load `stock-sentiment-analysis`.
   - If the user asks about **个股-板块-大盘共振**, a collective sector surge, or whether a sector/stock move can continue, load `stock-sentiment-analysis` and apply its `Market-Sector-Stock Resonance And Continuation` framework. Separate logic durability, tape continuity, and entry quality; do not infer a good entry from a good industry thesis.
   - Final answers should include a compact `融合口径` line when any supporting skill is used, e.g. `东财/公告/股吧证据 + macro-news-check tape + stock-technical-analysis 结构 + stock-sentiment-analysis 情绪周期`.

   Optional 东方财富妙想 enhancement: if the user has installed the `mx-*` A-share/financial skills in the current session or under the local skills directory, use them as a non-blocking data layer for A-share move reasons, sector mapping, valuation, financials, and current news checks. MX data supplements the existing know-how; it must not replace the normal Eastmoney/Guba/announcement collector, source hierarchy, A-share emotion-cycle framework, expectation-gap analysis, or technical/macro confirmation. If an `mx-*` skill is missing, unauthorized, over quota, or returns empty data, continue with the normal source/web workflow and do not claim that 妙想 data was used. You may briefly suggest installing or configuring 东方财富妙想 skills only when the missing layer would materially improve the user's exact request, such as A-share sector constituents, self-selected-stock filtering, timely financial data, or official finance-data search.

   Use the 妙想 skills this way:
   - `mx-data`: current/historical quotes, market cap, PE/PB, EPS/ROE/margins, share count, main-fund flow, index/sector/board quote data, and A-share financial statement metrics for valuation.
   - `mx-search`: latest news, announcements, research reports, policies, event explainers, and time-sensitive market/sector context.
   - `mx-xuangu`: sector constituents, concept-board candidates, peer lists, condition screens, and "same theme but stronger/weaker" comparisons. For A-share questions such as `这个板块有哪些股票`, `相关股`, `概念股`, `龙头股`, `板块成分`, or `同题材还有谁`, try `mx-xuangu` first when available, then use `mx-data`/`mx-search` to rank purity, heat, and catalysts.
   - `mx-zixuan`: only when the user explicitly asks to query/add/delete/filter their 东方财富 self-selected stocks. For `自选股里哪些符合条件`, first try a direct `mx-xuangu` query constrained to self-selected stocks; if unsupported, use `mx-zixuan` to get the self-selected list and intersect it with `mx-xuangu` results. Do not use it automatically for ordinary analysis because it touches user account data.
   - `mx-moni`: only when the user explicitly asks about simulated portfolio holdings, funds, orders, simulated buy/sell, cancel orders, or posting a simulated-trading note. Do not use it for real trading or ordinary analysis.

   Eastmoney Guba topic enhancement: when the stock's sector/theme reason is unclear, or when a move may be part of a broader A-share topic rotation, check `https://gubatopic.eastmoney.com/` as an optional topic-discovery layer. Use it to identify current market hotspots, possible next-day continuations, and what topics, concepts, or boards the market is discussing, then verify with actual stock/sector moves, announcements, formal news, and the collected evidence. Treat Guba topic heat as sentiment/topic evidence, not confirmed fact.

2. 先取得当前行情、公告、最近24小时新闻及最多100条股吧/资讯候选、最多10份相关公告；按需要补充指数、行业/概念、涨跌家数。只读单股材料的请求可跳过市场背景。通过当前可用网页/工具读取东财行情、公告与股吧；采集失败不等于没有消息。

3. Analyze the collected source material directly. Treat sources with this priority:

- Announcements, earnings, regulatory filings, and confirmed company materials: primary evidence.
- 妙想 `mx-data` / `mx-search` outputs, when available, can supplement or cross-check quote, financial, announcement, research, and event evidence. Use them as evidence with source attribution, but still distinguish official filings from media/research interpretation.
- Eastmoney 股吧资讯/high-read posts: secondary evidence; useful for discovering what the market is discussing.
- Eastmoney Guba topics (`https://gubatopic.eastmoney.com/`): secondary topic-discovery evidence; useful for mining possible themes and board-level reasons behind A-share moves, but must be verified against stock/sector price action and formal news.
- Sohu index and sector/concept board context plus Eastmoney intraday advance-decline counts and Sohu historical advance-decline / limit-up / limit-down data: market/sector backdrop only; use it to judge 共振 versus 独立催化.
- Ordinary 股吧 posts: emotion and speculation only. Never treat them as confirmed fact unless the same item appears in announcements/news.
- Macro tape: call `macro-news-check` only when the move may be affected by broad A-share risk appetite, policy/liquidity headlines, PBOC/CNY, commodities, US rates, Hong Kong/US China ADR moves, geopolitical risk, or sudden index/sector-wide news. Use it to judge market-wide pressure or support, not to replace announcements or stock-specific evidence.

4. Prefer this skill as the first pass for A-shares. When using `stock-sentiment-analysis`, `macro-news-check`, or `stock-technical-analysis`, first finish the stock-specific evidence read, then use the supporting skill to verify sentiment structure, broad-market pressure/support, or price confirmation. Do not replace confirmed announcements or filings with macro, sentiment, or chart evidence.

5. In multi-turn discussions about the same stock, treat user follow-ups as possible new evidence or feedback. If the user adds information, challenges the reasoning, asks for reconsideration, or the conversation reveals that the prior answer missed/misweighted something, re-evaluate the stock with the new context before defending the earlier answer.

## DTM API Context

Use the canonical JSON interfaces in `https://daytrading.monster/api-docs/` for DTM reads. `https://daytrading.monster/api/chinastock-anomaly` supplies current rising/falling themes, limit-up concepts, hourly ranking snapshots, individual move reasons, and limit-up rows; match the target code and snapshot time. Read `https://daytrading.monster/api/themes` without a market filter to trace cross-market industry-chain and theme transmission across China, Japan, and the US. Use `themes[]` and `constituents[]` for members, `weight`, `reason_zh`, coverage, and completed-session returns; check dates instead of treating them as live moves. Parse the `text/plain` response bodies as JSON. Do not use DTM institution-survey data.

## A-share Emotion Cycle

Classify the short-term emotion backdrop qualitatively into one of seven stages from the single-stock materials, price action, 股吧 discussion, market indexes, sector/concept boards, today's breadth, and recent Sohu zdt history:

1. `冰点期`: many limit-downs or large losers, high failed-board/亏钱效应, shrinking participation. Observe who resists the selloff.
2. `修复/潜伏期`: panic eases, limit-downs decrease, front-row names begin to rebound, but most traders are still skeptical. Small trial positions only.
3. `启动期`: new theme appears, first/second boards increase, capital starts focusing. Prefer front-row names in the core theme.
4. `加速期`: leaders continue limit-up, followers spread, sector赚钱效应 is strong. Hold strength, avoid random laggards.
5. `高潮期`: everyone discusses the theme, limit-up wave or one-word boards, retail emotion is hot. Take profits progressively; do not chase heavily.
6. `高位分歧/分化期`: after高潮, leaders may炸板/断板/long upper shadow while back-row names weaken, but the whole market has not fully collapsed yet. Treat it as the transition from emotion top to退潮.
7. `退潮期`: leaders break down, 天地板/核按钮 rise,亏钱效应 spreads. Reduce exposure or wait.

Useful loop: `冰点 -> 修复/潜伏 -> 启动 -> 加速 -> 高潮 -> 高位分歧/分化 -> 退潮 -> 再冰点`.

`分歧` is not always bearish. A healthy divergence during 启动/加速 can be a换手 test or main-line pullback before renewed agreement; a high-level divergence after高潮 is usually a risk signal. The favorable windows are usually late 修复 to early 启动, and healthy main-line divergence before 加速. The most dangerous windows are late 高潮, 高位分歧/分化, and early 退潮.

## Reading News And Emotion

- Separate `confirmed catalyst` from `market imagination`. A confirmed order, policy, earnings beat, regulatory approval, or buyback is stronger than a forum narrative.
- For each meaningful catalyst, do an expectation-gap check: `市场原来预期什么` -> `实际消息落地什么` -> `超预期 / 符合预期或只是落地 / 不及预期`. This applies to numeric news such as orders, earnings, guidance, policy size, and buybacks, and to qualitative news such as wording strength, timing, certainty, regulatory tone, management confidence, and whether the news solves the market's real concern.
- Use the emotion-structure checklist from [experience](references/experience.md): classify market phase, main-line versus defensive bucket, capital return frequency, breadth/赚钱效应, first healthy divergence versus high-level divergence, institution-style trend versus 游资PK, and whether a rebound is new leadership or old-leader exit liquidity.
- Decide whether the stock is an `情绪票` or a `趋势票`:
  - 情绪票: topic-driven, high volatility, limit-up relay, fast climax/retreat.
  - 趋势票: supported by industry cycle, earnings, policy, or institutional logic; slower but more durable.
- Watch for emotional-top clues: high attention, continuous large candles, high turnover, failed breakout, long upper shadow, break-board/炸板, or broad follower exhaustion.
- Watch for trend-risk clues: good news priced in, valuation stretch, volume-price divergence, loss of key moving averages, or gradual weakening after a crowded story.

## Output Style

Reply in Chinese unless the user asks otherwise. The answer can be detailed because this is a single-stock local script workflow. Use this order:

1. `最有力理由`: most likely catalyst, with source names and timing.
2. `补助理由`: secondary drivers such as theme, sector rotation, liquidity, valuation, or positioning.
3. `共振判断`: whether the stock is moving with the market, its sector/concept, or mostly on stock-specific news. When continuation matters, structure this as `market -> sector/theme -> stock` and apply the shared six-factor resonance framework from `stock-sentiment-analysis`.
4. `情绪面/周期位置`: qualitative 股吧 emotion plus the seven-stage A-share emotion cycle.
5. `确定度`: high / medium / low, with one sentence explaining why.
6. `注意点`: what remains unconfirmed or what could invalidate the read.

If evidence is weak, say so plainly and use wording like `思惑`, `低信息量`, `未确认`, or `确认待ち`. Do not invent catalysts absent from the collected evidence.

## Valuation Requests

When the user asks for `合理估值`, `目标价`, `估值`, `贵不贵`, `空间`, `fair value`, or similar:

- Still collect current quote/news/公告/股吧/market-context materials first, then add financial guidance, EPS/share-count, capital policy, and peer/sector context when available.
- Use the `Reasonable Valuation Framework` from [experience](references/experience.md).
- Provide scenario ranges rather than one exact target: conservative / base / bull.
- State the anchors used, such as forward EPS/PE, operating profit, ROE/PB, EV/EBITDA, orders/backlog, buyback/convertible bond dilution, and peer multiples.
- When using EPS/PE, explicitly decompose price into `EPS x PE`: judge whether the setup is a Davis double play (`EPS upgrades + PE expansion` from better growth/certainty/theme premium) or Davis double kill (`EPS downgrades + PE contraction` from weaker guidance/cycle reversal/expectation miss). Do not call a stock cheap from PE alone if EPS or the deserved multiple is falling.
- Explicitly separate fundamental fair value from A-share emotion-cycle premium/discount.
- Explicitly say what the current price already prices in, what must happen to justify upside, and what would invalidate the valuation.
