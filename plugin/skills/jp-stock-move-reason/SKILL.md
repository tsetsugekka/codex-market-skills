---
name: jp-stock-move-reason
description: 分析日本股票上涨下跌、财报反应和PTS异动，核验公司披露、预期差、量价及市场背景。
---

# JP Stock Move Reason

## 跨环境执行

先按[环境能力路由](../market-daily-strategist/references/runtime-capabilities.md)发现当前会话已安装、已连接且有权限的 Skill、工具、网页和计算能力。OpenD/moomoo、妙想、同花顺等是可选数据能力；不能由 ChatGPT Web、工作环境或 Codex 的名称推定可用性。优先复用已取得且仍有效的资料。研究来源顺序、字段与计算方法不因环境不同而省略；缺能力时说明具体缺口，不宣称已采集或已计算。

此包按各 Skill 入口附带可移植 Python 脚本；可读取文件不等于能执行，能执行不等于能联网。先确认能力，再按环境路由选择随包脚本、可用扩展或公开网页；仅有用户资料时执行相同筛选与计算，无执行能力时按文字流程研究并标出未计算项。外部供应商采集器只在已安装且可用时调用。访问失败、限流与权限处理遵循当前工具及环境规则，不复制机器专用沙箱设置。实际加载所用的同包 Skill 和参考，不只在回答中提名字。

本插件用于研究，写日历、账户或交易需要对应授权。普通研究不自动访问私人自选或持仓，不修改自身、其他 Skill 或任务规则；自动任务保持自己的输出、归档和授权合同。用户指定的私人资料仅在本轮授权范围内使用，不写入插件。

Use this skill to explain current single-stock moves from source evidence.

## Workflow

1. Read [experience](references/experience.md) before analysis, but only the `Active Playbook` sections unless the user explicitly asks for historical lessons. Apply those lessons when setting expectations, especially around earnings, guidance, valuation, 掲示板 sentiment, theme leadership, peer follow-through, and whether the stock is a leader, follower, defensive alternative, old-leader rebound, or noise. When the request needs a deeper or reusable sentiment framework, also use `stock-sentiment-analysis` and its `references/sentiment-framework.md`.

   Cross-skill calls are operational. When this workflow says to use another market skill, actually load that skill's `SKILL.md` and required references when available in this package or environment. Do not merely mention the other skill by name in the answer.

   Required coordination: for Japanese stock analysis, use this skill as the evidence-gathering entry point, and add supporting skills based on clues found during analysis, not only on the user's wording. Yahoo 掲示板 itself is an evidence source, not an automatic trigger for sentiment analysis. If 掲示板/news reveals a concrete clue about theme leadership, peer follow-through, crowding, leader/follower position, defensive alternative, old-leader rebound, or risk-on/risk-off acceptance, load `stock-sentiment-analysis` to test that clue. If 掲示板/news discusses Nikkei/TOPIX, JPX sectors, Nikkei futures, JGB yields, USD/JPY, BOJ/MOF policy, US/China spillover, commodities, or geopolitics, load `macro-news-check` to verify the tape instead of accepting forum claims. If 掲示板/news or the price move points to support/resistance, failed breakout, trend damage, or catalyst acceptance/rejection, load `stock-technical-analysis` to verify the chart. When the original question is directly about an index/broad tape such as Nikkei 225, TOPIX, JPX sectors, Nikkei futures, or 日经大盘, load `macro-news-check` by default.

   Mandatory execution gate:
   - If the answer uses **宏观** or **快讯** to explain the stock, sector, Nikkei/TOPIX, JGB yields, USD/JPY, BOJ/MOF policy, US/China spillover, commodities, or geopolitics, load `macro-news-check`. Do not replace this layer with ad hoc web search.
   - If the answer uses **技术面** such as support/resistance, trend confirmation, failed breakout, volume-price behavior, intraday timing, or "能不能上/下", load `stock-technical-analysis`.
   - If the answer uses **情绪面** such as theme leadership, crowding, leader/follower, defensive alternative, old-leader rebound, risk-on/risk-off, expectation gap, or 掲示板 psychology, load `stock-sentiment-analysis`.
   - Final answers should include a compact `融合口径` line when any supporting skill is used, e.g. `Yahoo/Kabutan/Traders 证据 + macro-news-check tape + stock-technical-analysis 结构 + stock-sentiment-analysis 情绪/期待差`.

2. Collect current quote, news/disclosures and forum evidence with the tools available in this session. For Python collection or offline forum filtering, read [Python execution](references/python-execution.md). For a single stock, verify concrete catalysts against disclosures before treating forum discussion as evidence.

### Mover Estimated Trading Value Ranking Sub-skill

When the user asks for current Japanese-stock increase/decrease Top10 lists,
PTS mover lists ranked by `推定成交额`, `売買代金推定`, `turnover estimate`, or
says `不是成交量，是成交额`, use the mover-turnover sub-skill before running
per-stock reason collection. Read
[pts-turnover-ranking](references/pts-turnover-ranking.md) and [Python execution](references/python-execution.md), then collect the matching session.

Default to `--session auto` and evaluate routing in JST on trading days:

- `09:00-11:30` and `12:30-15:30`: use Yahoo Finance Japan's current regular
  market rankings:
  `https://finance.yahoo.co.jp/stocks/ranking/up?market=all` and
  `https://finance.yahoo.co.jp/stocks/ranking/down?market=all`.
- `08:00-09:00`, `11:30-12:30`, and `15:30-17:00`: use the PTS day-section
  increase/decrease pages.
- All other times, weekends, and known non-trading days: use the PTS night
  section. The script handles weekends; force `--session night` on Japanese
  exchange holidays that fall on weekdays.

Always request 50 rows per page. First filter each side to `abs(涨跌幅) >= 3%`
and `出来高 > 2000`, then rank by estimated trading value. If one side has
fewer than five qualifying rows, re-fetch only that side to `abs(涨跌幅) >= 1%`
and keep ranking by estimated trading value. Regular-session `推定成交额`
(`売買代金推定`) is `当前价 * 出来高`; PTS `推定成交额` is
`PTS株价 * PTS出来高`. It is not exchange-reported trading value calculated
from each execution. Yahoo states that Tokyo Stock Exchange transaction prices
are real time while all-market volume is delayed by at least 15 minutes, so
regular-session output must disclose that mixed-timestamp limitation. Volume is
only the eligibility filter. For a generic Top10 request, or when the user
loosely says `成交量` within this workflow, still rank by `推定成交额`. Rank by
raw volume only when the user explicitly requests a volume-ranked list.

After ranking, final mover answers must include a `原因` column unless the
user explicitly says they only want the raw list, only want numbers, or do not
need reasons. For ranking requests, Yahoo 掲示板 is the first source for discovering explanation candidates, not the authority for confirming facts:
deduplicate selected Top codes and request one forum page per code, caching at
most the latest 100 comments each, using forum-only collection. For every
individual stock and every selected Top10 name, use the same comment pipeline:
count how many of those raw cached posts are within 24 hours; if fewer than 100,
expand the candidate window to 72 hours using only the same cached posts. Never
fetch post 101 or later. Apply the five-like minimum only after deciding the time
window, then score by recency, likes, body length, and company-material keywords,
deduplicate exact normalized-prefix signatures to a maximum 20-comment full-text
shortlist, reorder it by time and likes, and pass only `recent_comments[:5]` to
the assistant.
Process codes sequentially;
do not use Kabutan/Traders as the first-pass substitute for board discussion.

Use this exact comment-quality contract. Hard-filter posts outside the selected
window, unparseable timestamps, fewer than five likes, bodies shorter than ten
characters, and pure calls such as `買い`, `売り`, `上がれ`, `S高確定`,
`ストップ高`, `爆上げ`, `爆益`, `草`, or standalone `www`. Score surviving
posts out of 18: recency `<=6h:5`, `<=24h:4`, `<=48h:2`, `>48h:1`; body length
`30-300:3`, `>300:2`, `10-29:1`; likes `100+:4`, `50-99:3`, `20-49:2`,
`5-19:1`; company-material keywords add one point each, capped at six. Relevant
keywords include earnings, guidance revisions, dividends, buybacks, splits,
alliances, orders, approvals, patents, IR, profitability, M&A, subsidies,
adoption, launches, joint development, contracts, products/services, shareholder
benefits, revenue, and profit metrics. Generic sector words such as AI,
semiconductors, defense, or drones add no points. Sort by total score, timestamp,
then likes; normalize lowercase text by removing spaces and common punctuation,
deduplicate on the first 60 normalized characters, and keep at most 20. Finally,
sort those 20 by timestamp and likes and pass `recent_comments[:5]` to the assistant.
This is exact-signature deduplication, not semantic similarity: remove all
whitespace and `、。！？ ! ? , . ・ … 「」 『』 （） () [] 【】`, then compare the
first 60 normalized characters. The earlier comment in the score/timestamp/likes
order wins. Matching prefixes collapse even when later text differs; any
difference within the prefix survives. Do not apply Unicode width normalization
or explicitly strip emoji, URLs, or usernames. Deduplicate only within the
current stock's current collection.

Use news or disclosures only to validate a concrete event claimed in the board,
and distinguish verified facts from market discussion. Never fetch more than one
forum page per code or repeat a forum fetch for the same code in the same turn.
On HTTP 403/429, access-denied content, connection reset, or an empty/abnormal
response, stop all Yahoo collection for the rest of the turn and report the
block. ETF or ETN rows should be explained from their underlying index/strategy,
and tiny-estimate jumps should be labeled low-confidence if no hard catalyst exists.

Return the synthesized `原因` in the ranking table. Do not quote or enumerate the
raw five-comment input set unless the user explicitly asks to see it.

Space sequential Yahoo requests by 1–3 seconds; after 403/429 or access-control content, stop Yahoo requests for the turn. Preserve any cooldown enforced by the actual tool.

- DTM cross-market themes: read `https://daytrading.monster/api/themes` without a market filter. Compare Japanese, US, and Chinese theme members and completed-session performance to trace industry-chain and cross-market transmission; use `themes[]` with `theme_key`, `theme_name_zh`, `market`, and `constituents[]`, including `weight`, `reason_zh`, and `quote_available`. Check quote dates; these are not live intraday returns.
- PTS context: prefer the canonical `https://daytrading.monster/api/pts/model1` (day session), `https://daytrading.monster/api/pts/model2` (after close), and `https://daytrading.monster/api/pts/model3` (night session) for a comprehensive overview of PTS risers, themes, and upward reasons. Use the session(s) relevant to the question and their update times; read all three when comparing sessions. They do not provide a complete falling-stock ranking. For diverse Japanese rankings, including PTS decliners and other screens, use `https://kabutan.jp/warning/` and `https://finance.yahoo.co.jp/stocks/ranking/up`, selecting the relevant ranking and its stated session. Keep the existing estimated-turnover Top10 procedure for that specific request.

### Evidence priority for individual stocks

Analyze the collected source material directly. Company disclosures and confirmed event reporting establish facts; quotes establish the move. Forum-first ranking discovery above does not override this factual priority:

- Current quote and basic metrics: establish whether there is a real price move and the stock's size/liquidity context.
- Institution rating check: after reading current source evidence, read only the canonical `https://daytrading.monster/api/ratings-jp` JSON from `https://daytrading.monster/api-docs/`. Parse the `text/plain` body as JSON. Its `reports` cover Japan-local today and the preceding three calendar days; use the report date, not retrieval time. No additional rating-page files are needed.
  Filter by exact normalized `stockCode` and use only reports present in the current snapshot. Mention the rating layer only when the stock has a current matching rating/target-price update that may explain or support the move. If there is no matching current update, omit the rating layer instead of writing negative filler. When the rating layer is mentioned, include broker, date, rating direction, target-price direction, and whether the update is likely a primary catalyst or secondary support. In final answer prose, do not name DayTrading.monster, the rating page, feed/page labels, or aggregator/source names by default; Cite material claims with the actual source URL and time.
- PTS handling: during the regular Tokyo trading session, especially the opening and active intraday period, do not use PTS as an analysis layer; prioritize the live exchange quote, intraday price action, volume, news, and 掲示板 instead. For questions asked after the Tokyo close, check the Kabutan individual stock page (`https://kabutan.jp/stock/?code=CODE`) when available. Use the page's `PTS` block sourced from JapanNext via Kabutan for PTS current price, timestamp, open/high/low, volume, trading value, and VWAP, but remember Kabutan's PTS figures are delayed by about 15 minutes. Treat PTS as delayed early after-hours sentiment and liquidity evidence, not as a confirmed next-session price or real-time tape. If using DTM PTS to discover candidates, read the canonical model APIs above; do not use the HTML `noscript` SEO fallback because it can lag the live app. Do not use MONEY BOX PTS as a source because its PTS figures have proven unreliable; non-PTS MONEY BOX pages such as disclosure summaries may be used only as supplementary references and should be verified against primary disclosures/news.
- Company disclosure and explanation materials: for earnings, guidance revisions, medium-term plans, business updates, buybacks, major orders, capital policy, or new businesses, look beyond headline numbers and 掲示板. Search TDnet/Kabutan PDFs, the company's IR site, 決算説明資料, 補足説明資料, 事業計画及び成長可能性に関する事項, 中期経営計画, 決算説明会資料/Q&A, press releases, product/project pages, and business-update materials. Use these to explain what changed in the business story, pipeline, certainty, timing, customer/project progress, capital needs, and dilution risk.
- News: primary evidence for concrete catalysts.
- Yahoo 掲示板: use only as a low-weight retail emotion/overheating check. Its buy/sell sentiment is delayed, reflects only past retail verbal mood, and should not be used as evidence for a price move, catalyst, conviction, or directional thesis. Never cite 掲示板 buy/sell ratios as support for an analysis. Use comments only to detect what retail is talking about, whether attention is crowded, or whether rumor risk needs verification against news/disclosures.
- Peer and theme reactions: use them to judge whether the move is theme-wide leadership, same-theme follow-through, or only stock-specific sentiment.
- Macro tape and Japan market breadth: call `macro-news-check` only when the move may be affected by Nikkei/TOPIX futures, JGB yields, USD/JPY, BOJ/MOF policy, global rates, China/US macro, commodities, geopolitical risk, or broad risk-on/risk-off headlines. For Japanese broad-market weakness/strength or a single-stock move under strong market pressure, use the JPX real-time index page/data (`https://www.jpx.co.jp/markets/indices/realvalues/index.html`, `indices_stock_price3.txt`, and `indices_stock_price3.time.txt`) as an auxiliary confirmation layer for TOPIX 33 sectors, TOPIX-17, size indexes, and market-type indexes. Use it as market context, not as a substitute for stock-specific evidence.

For earnings-related questions, do a disclosure-material pass even when the user did not explicitly ask for it. The core question is not only `数字好不好`, but `为什么这些数字或指引可信`, `哪些说明资料证明业务进入兑现阶段`, `哪些项目仍只是 pipeline`, and `现金流/融资/稀释/客户集中是否会削弱估值`. If no explanation material exists, say so and rely on the filing, company releases, and news.

Prefer this skill as the first pass for Japanese stocks. When using `stock-sentiment-analysis`, `macro-news-check`, or `stock-technical-analysis`, first finish the news/disclosure/theme/rating read and use 掲示板 only as a retail heat check, then use the supporting skill to verify sentiment structure, broad-market pressure/support, or price confirmation. Do not replace company disclosures, concrete news, or fresh rating updates with macro, sentiment, chart evidence, or 掲示板 chatter.

In multi-turn discussions about the same stock, treat user follow-ups as possible new evidence or feedback. If the user adds information, challenges the reasoning, asks for reconsideration, or the conversation reveals that the prior answer missed/misweighted something, re-evaluate the stock with the new context before defending the earlier answer.

## Output Style

Reply in Chinese unless the user asks otherwise. The answer can be detailed when the evidence supports it: start from at least 3-4 lines, and when evidence is rich, write up to the length of a short market news note. Stay evidence-based.

For an individual-stock explanation, use these five sections unless the user or Task supplies a different format. For a ranking, use the table format above:

1. `最有力理由`: the most likely catalyst, with source names and timing.
2. `补助理由`: secondary drivers such as theme buying, short-term speculation, or market-cap/liquidity context.
3. `掲示板温度`: summarize heat level, recent post volume, high-like comments, expectation gap, and crowding risk.
4. `确定度`: high / medium / low, with one sentence explaining why.
5. `注意点`: what remains unconfirmed or what could invalidate the read.

When the user gives multiple stocks, write the five numbered sections separately for each stock first. After all individual stock sections, add a final comparison section such as `两只对比` or `多只对比`, covering common drivers, differences in catalyst quality, sentiment heat, and relative risk. You may add extra sections when useful, while preserving the same evidence, uncertainty and comparison content.

If the evidence is weak, say so plainly and use wording like `思惑`, `期待`, `传闻`, or `确认待ち`. Do not invent catalysts absent from the collected news/comments.

When explaining a catalyst, always check the expectation gap: `市场原来预期什么` -> `实际消息落地什么` -> `超预期 / 符合预期或只是落地 / 不及预期`. This applies to numeric news such as guidance, earnings, orders, dividends, and buybacks, and to qualitative news such as wording strength, timing, certainty, management confidence, regulatory tone, and whether the news solves the market's real concern.

## Valuation Requests

When the user asks for `合理估值`, `目标价`, `估值`, `贵不贵`, `空间`, `fair value`, or similar:

- Still collect current quote/news materials first, then add financial guidance, EPS/share-count, capital policy, and peer/sector context when available.
- Use the `Reasonable Valuation Framework` from [experience](references/experience.md).
- Provide scenario ranges rather than one exact target: conservative / base / bull.
- State the anchors used, such as forward EPS/PER, operating or recurring profit, ROE/PBR, EV/EBITDA, orders/backlog, buyback/CB dilution, and peer multiples.
- When using EPS/PER, explicitly decompose price into `EPS x PER`: judge whether the setup is a Davis double play (`EPS upgrades + PER expansion` from better growth/certainty/theme premium) or Davis double kill (`EPS downgrades + PER contraction` from weaker guidance/cycle reversal/expectation miss). Do not call a stock cheap from PER alone if EPS or the deserved multiple is falling.
- Explicitly say what the current price already prices in, what must happen to justify upside, and what would invalidate the valuation.
