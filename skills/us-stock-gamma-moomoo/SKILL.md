---
name: us-stock-gamma-moomoo
description: Analyze US stock and ETF option gamma exposure with moomoo OpenD, plus .SPX/SPXW index-option structure using SPY/ES/CFD conversion when needed. Use when the user asks for gamma, GEX, gamma wall, gamma flip, SPX/SPY/ES intraday gamma, 0DTE option scenario value tables, option positioning, US-stock dark pool/off-exchange flow, borrow fee, FTD, short volume, or ChartExchange confirmation. Produces plain-language text conclusions from moomoo option chain, snapshots, Greeks, OI, IV, and pre-market/latest stock price; raw JSON is only for explicit export requests.
metadata:
  version: 0.1.5
---

# US Stock Gamma With moomoo

Use this skill to turn moomoo OpenD option data into an actionable gamma map and a plain-language trading note.

This public-safe skill is self-contained. Do not commit personal information, API keys, account data, private RAG files, or private research materials to GitHub. It may use a user-specified private RAG folder during a session, but it must not store private source paths, personal positions, original strategy names, private person names/handles, proprietary labels, or private document titles. Generic market concepts such as gamma, GEX, dealer hedging, FVG, KDJ, MACD, RSI, VWAP, and Vegas may be retained.


## Public And Private Versions

If both public and private versions of this skill exist, prefer the private version for local analysis when the user permits it. The private version may use local RAG indexes and user-specific study material.

When updating the skill, keep public and private versions in sync: write public-safe, generalized lessons to the public version; keep private labels, private paths, raw notes, screenshots, account data, and personal trade context only in the private version or private RAG index.

When preparing a GitHub upload or public release, use the public version only and run the repo-level release/privacy check from the repository root at `shared/references/release-and-privacy.md`. Never upload private RAG folders, `.ftindex` files, credentials, `.env`, personal data, screenshots, raw PDFs/PPTs, or private strategy labels.

## Experience

Before deep analysis, read `references/experience.md` if it exists, but only `Active Playbook` and `Compression Protocol` unless the user explicitly asks for historical lessons. If a multi-turn correction produces a durable reusable lesson about gamma interpretation, option scenario handling, news/gamma interaction, or chart confirmation, update that file after answering. Generalize the lesson and strip private details.

Cross-skill calls are operational. When this workflow says to use another market skill, actually load that skill's `SKILL.md` and required references if the skill is installed or available as a sibling in this repository. Do not merely mention the other skill by name in the answer.

Required coordination: for US option/gamma analysis, use this skill as the positioning and option-structure entry point, and add supporting skills based on the analysis workflow, not only on the user's wording. If the analysis is about SPX, SPXW, SPY, QQQ, Nasdaq, Dow, Russell, VIX, Nikkei proxy gamma, or any broad index/ETF gamma map, load `macro-news-check` because index gamma cannot be read well without current macro and broad-market tape. If the analysis discusses news acceptance, theme crowding, risk-on/risk-off tone, forum/social sentiment, or leader/follower context, load `stock-sentiment-analysis`. If the final view depends on support/resistance, intraday timing, trend confirmation, failed breakout, or price-action validation, load `stock-technical-analysis`. Gamma is the positioning map; macro, sentiment, and chart structure decide whether the map is being accepted or rejected.

When official moomoo anomaly skills are installed, use them as an auxiliary scan layer, not as a replacement for the self-calculated gamma map. For user requests involving `异动`, `大单`, `IV`, `PCR`, `聪明钱`, unusual options activity, option sentiment, or volatility anomaly, call `moomoo-derivatives-anomaly` alongside this skill by default. For U.S. stocks, do not request Hong Kong-only warrant / CBBC dimensions; use only U.S.-applicable option dimensions such as `option_unusual`, `option_volatility`, `option_volume_price`, `option_sentiment`, and `option_comprehensive`. A full scan can fail if it includes Hong Kong-only dimensions, so narrow the dimensions explicitly when needed.

If the analysis uses 1-minute K-line confirmation from moomoo OpenD, coordinate with `stock-technical-analysis`: let this skill fetch or compute the option/gamma map, then use the technical skill's framework to judge whether price action accepts, rejects, or only probes a wall, pit, or flip. If the user asks why a U.S. stock moved, whether earnings/guidance/news were accepted, or what explains a price move, route the evidence-gathering entry point to `us-stock-move-reason` first, then use this skill only for the option-positioning layer.

For ordinary U.S. stock move analysis, ChartExchange-style off-exchange/dark-pool data can be a secondary confirmation layer when price action or option positioning leaves an open question. Use it after confirmed news, macro/sector tape, price/volume, and option/gamma evidence. It is most useful for hidden-liquidity context around unusual volume, unexplained moves, failed news reactions, squeeze candidates, or repeated support/resistance at specific prices.

## Mandatory Execution Gate

Before running scripts or writing the final answer, classify the request and load required sibling skills:

- **Broad index / ETF gamma** (`SPX`, `SPXW`, `SPY`, `QQQ`, `Nasdaq`, `Dow`, `Russell`, `VIX`, `Nikkei`): load `macro-news-check` first or in parallel, then explicitly merge the macro tape with the gamma map. Do not answer index gamma from gamma data alone.
- **宏观 / 快讯 / rates / FX / commodities / geopolitics / Fed / yields**: load `macro-news-check`. Do not substitute ad hoc web search for this layer.
- **技术面 / intraday execution / "now" / support-resistance / "can it get through" / price action**: load `stock-technical-analysis` unless the user asks for a pure option-positioning dump. Use price action to decide whether a wall/pit is accepted, rejected, or only a battlefield.
- **官方 moomoo 期权异动 / 大单 / IV / PCR / 聪明钱**: when `moomoo-derivatives-anomaly` is available, run it as a parallel anomaly scan using U.S.-applicable option dimensions only; do not include Hong Kong warrant / CBBC dimensions for U.S. stocks.
- **情绪面 / news acceptance / crowding / risk-on or risk-off psychology / expectation gap**: load `stock-sentiment-analysis` when sentiment or expectation gap changes the interpretation.
- **新闻接受度 / 财报 / 指引 / 股价为何涨跌**: use `us-stock-move-reason` as the upstream catalyst workflow, then merge its evidence with this skill's gamma map.
- **Dark pool / off-exchange / borrow / FTD / short-volume checks for U.S. stocks**: use ChartExchange or the original FINRA/borrow-data source only as a secondary positioning layer. Do not use dark-pool prints or off-exchange share alone as a bullish/bearish signal.
- If a required sibling skill is unavailable, say so and provide a limited gamma-only read. If it is available but not needed, state the reason briefly.

Final answers for index gamma should include a compact `融合口径` line naming the layers used, for example: `自算 SPXW gamma + macro-news-check tape + stock-technical-analysis price action + stock-sentiment-analysis emotion/expectation gap`. This makes skipped or missing skill fusion visible.

## Environment Check

This skill requires moomoo OpenD plus the Python SDK/skills environment.

- First check whether OpenD is running and the `moomoo` Python package imports. If not, guide the user to install or launch OpenD using the `install-moomoo-opend` skill.
- Tell the user OpenD must stay running in the background while querying quotes/options. Login may be required for permissioned data.
- Do not ask the user to unlock trading or input an encrypted private key unless they explicitly want trading functions. This skill only needs quote/option data.
- If moomoo cannot provide a live index snapshot, use available option chains plus a user-provided/live SPX, ES, CFD, or SPY anchor and state the anchor clearly.
- For live 1-minute K-line confirmation through OpenD, treat subscriptions as reusable runtime state, not as permanent skill state. Prefer reusing an existing `US.SPY` `SubType.K_1M` subscription during a live OpenD session; if `get_cur_kline(code, n, KLType.K_1M, AuType.QFQ)` returns `请先订阅KL_1Min数据` or another stale-subscription/permission error, call `subscribe([code], [SubType.K_1M], subscribe_push=False)` and retry once. OpenD subscriptions may disappear after OpenD restart, reconnect, quota changes, permission changes, or context lifecycle changes, so do not write "currently subscribed" as a static fact into the skill or output.

## Default Output

Route the request before choosing a script:

- **Ordinary US stocks/ETFs**: use `scripts/gamma_report.py`.
- **SPX / SPXW / SP500 / 标普500 / S&P 500 index gamma**: do not use `gamma_report.py` as the final workflow. Use `scripts/spx_intraday_latest.py` and `references/spx-intraday.md`: query `US..SPX`, keep SPX/SPXW strikes directly, infer the spot anchor from SPXW 0DTE put-call parity when the SPX index snapshot is unavailable, and treat SPY only as a sanity check or fallback.
- **Nikkei / 日经 / 日経 / NKY / Nikkei 225 index gamma**: do not present raw EWJ ETF strikes as index levels, and do not use a current Nikkei anchor against a stale EWJ close. Use EWJ only as a proxy option book, then convert with a time-aligned bridge: EWJ quote-time value -> `NKDmain`/Nikkei futures at that same time -> current `NIYmain`/Nikkei CFD or the user's current index anchor. Use `scripts/proxy_index_gamma.py`. The report must state every anchor, ratio, timestamp, and limitation.

Default to a concise chat/terminal text summary. Do not create files as part of this skill unless the user explicitly requests raw JSON export.

For ordinary US stocks/ETFs use `scripts/gamma_report.py` when the user asks for the ticker itself:

```bash
python3 ~/.codex/skills/us-stock-gamma-moomoo/scripts/gamma_report.py US.BA
python3 ~/.codex/skills/us-stock-gamma-moomoo/scripts/gamma_report.py US.MP
```

For SPX/SPXW intraday index gamma use:

```bash
python3 ~/.codex/skills/us-stock-gamma-moomoo/scripts/spx_intraday_latest.py
```

When the user asks about `未来几天 gamma`, `未来几日 gamma`, `后面几天 gamma`, `按日期看 gamma`, `哪天强哪天弱`, or shares a multi-expiry gamma chart and wants the forward read, use the per-expiry report mode:

```bash
python3 ~/.codex/skills/us-stock-gamma-moomoo/scripts/spx_intraday_latest.py --by-expiry-report
```

When comparing against an earlier same-day SPX/SPXW snapshot, pass the previous JSON and any specific battlefield strikes the user cares about:

```bash
python3 ~/.codex/skills/us-stock-gamma-moomoo/scripts/spx_intraday_latest.py \
  --compare-json /path/to/previous_spx_gamma.json \
  --watch-strikes 7400,7425,7450
```

For Nikkei 225 proxy gamma using EWJ converted to a Nikkei CFD/index anchor use:

```bash
python3 ~/.codex/skills/us-stock-gamma-moomoo/scripts/proxy_index_gamma.py US.EWJ \
  --index-name "日经225 / NKD-NIY proxy" \
  --bridge-anchor-at-proxy-time 59920 --bridge-current 60110 --final-anchor 60080
```

The script:
- reads stock snapshot, option expirations, option chain, option snapshots, and daily K lines from moomoo OpenD;
- throttles `get_option_chain` calls and retries once after OpenD frequency-limit errors, because moomoo can reject more than about 10 option-chain requests in 30 seconds;
- uses `pre_price` when available, otherwise bid/ask midpoint, otherwise regular-session last price;
- gathers option `OI`, `IV`, `delta`, `gamma`, `theta`, `vega`, bid/ask, volume;
- calculates Black-Scholes vanna from live/anchor spot, strike, IV, and DTE because moomoo snapshots may not provide `option_vanna`;
- selects option expiries by default as: all weeklies within the next 2 calendar weeks when available, plus monthly expiries for the current month and next 2 months; for high-frequency option names also include the next 2 trading-day/daily expiries when listed;
- calculates signed GEX with the common assumption `Call = +`, `Put = -`;
- calculates signed VEX with the same directional convention, expressed as spot-equivalent delta-dollar change per 1 vol point IV move;
- recomputes gamma across a spot-price grid to estimate gamma wall, gamma trough, and gamma flip;
- when JSON output is requested, includes per-strike `gex_by_strike` and `vex_by_strike` for each bucket so later runs can detect same-strike support/risk migration instead of only comparing top walls and pits;
- includes a `per_expiry` section in JSON for each selected expiration date, so future-days gamma reads can say which exact date is weaker or stronger instead of only using `Next2` / `Fri2w` aggregate buckets;
- with `--by-expiry-report`, prints a per-date forward gamma memo that names each selected expiry date, net GEX, flip, main downside risk zone, upper pressure/pinning zone, and a baseline/bearish/repair scenario;
- with `--compare-json`, compares the new snapshot with a prior JSON snapshot and highlights material strike-level changes, including positive-to-negative GEX flips where a prior support/wall has disappeared and become a pit or acceleration risk;
- prints a readable text memo by default; JSON export flags should be used only when the user explicitly asks for raw data.

For SPX 0DTE or quick trading questions, chat/terminal text is the default. Still compute or fetch the chain first when possible.

For short-dated option value scenarios, use `scripts/option_scenario_table.py` after fetching live IV/spot from moomoo:

```bash
python3 ~/.codex/skills/us-stock-gamma-moomoo/scripts/option_scenario_table.py \
  --kind C --strike 7370 --iv 16.8 \
  --asof 2026-05-13T02:30:00+09:00 --expiry 2026-05-13T05:00:00+09:00 \
  --spots 7350,7360,7370,7380,7390
```

Read extra references only when the request needs them:

- For `.SPX`, `SPXW`, `SPY`, `ES`, SpotGamma/TRACE heatmap, or intraday index judgment, read `references/spx-intraday.md`.
- For short-dated option value tables, account-recovery option targets, or “what is this call/put worth if price reaches X by time Y”, read `references/option-scenario-tables.md`.
- For U.S. single-stock dark-pool/off-exchange, borrow-fee, short-volume, FTD, or ChartExchange confirmation, use the `Dark Pool / Short Data Layer` section below.

## Text Level Map And Session Memory

For SPX/SPXW and other index-style intraday gamma answers, expose the level work as text: short bullets, compact Markdown tables, and a direct bias line. Do not rely on visual-only interpretation.

For forward-looking requests such as `未来几天 gamma`, `未来几日 gamma`, `后面几天 gamma`, `哪天强哪天弱`, or a screenshot showing several expiry dates, do not answer only with `0DTE / Next2 / Fri2w` tables. Use `spx_intraday_latest.py --by-expiry-report` or otherwise compute `per_expiry`, then answer in this structure:

1. Start with one sentence: `从“未来几天 gamma”角度看：...` and say whether the next 1-3 days are repaired, weak, high-volatility, or pressure-first. Name the key repair zone.
2. Add `按具体到期日看：` and one short paragraph per expiry date, e.g. `2026-06-09 周二，当天到期`, `2026-06-10 周三`, `2026-06-11 周四`, `2026-06-12 周五`. For each date, state: weak/strong label, net GEX direction and rough size, flip, main downside put-gamma risk zones, upper call-gamma pressure/pinning zones, and what price must reclaim to improve.
3. Add `我的推演：` with exactly three scenario bullets: `基准情形`, `偏空情形`, and `修复情形`. These scenarios should use dates and levels, not generic statements.
4. End with a plain conclusion such as: `所以按日期结论是：周二最弱，周三/周四仍偏压制，周五有修复窗口但门槛在 7450。`

For this mode, avoid dumping every strike or table row. The user wants the trading meaning: which date is structurally weak, where risk migrates, where repair starts, and what would invalidate the weak/strong read.

Key calculated levels:

- Prior-session pivot map: use the prior regular-session high/low/close when available. `PP = (H + L + C) / 3`, `BC = (H + L) / 2`, `TC = 2 * PP - BC`, `R1 = 2 * PP - L`, `S1 = 2 * PP - H`, `R2 = PP + (H - L)`, `S2 = PP - (H - L)`. For Camarilla, use `unit = 1.1 * (H - L) / 12`, then `H3 = C + 3 * unit`, `H4 = C + 4 * unit`, `H5 = C * H / L` when stable, `L3 = C - 3 * unit`, `L4 = C - 4 * unit`, `L5 = C - (H5 - C)`.
- CPR interpretation: narrow `TC-BC` means a larger directional expansion is easier; wide CPR means more chop/mean reversion. Spot above `TC` is constructive, between `TC/BC` is a balance zone, and below `BC` is weaker unless reclaimed.
- Gamma map: wall above spot is pressure or pinning; wall below spot is support or a recapture zone; negative pit below spot is acceleration risk; flip is the regime divider. Say whether the current spot is above/below flip and whether GEX is strengthening or weakening.
- Vanna map: combine top positive/negative VEX zones with IV direction, spot versus flip, and price action. Do not describe VEX alone as bullish or bearish.
- Rough magnet/bias: if enough strike-level GEX/VEX data is available, estimate a self-calculated magnet from dominant nearby walls, pits, and VEX zones using distance decay around current spot. Label it as rough and non-proprietary. Report it as `magnet above/below current spot`, plus a plain bias such as `偏多修复`, `中性钉扎`, `上方压力`, or `下方加速风险`.

When the user runs this skill multiple times during the same trading day in the same conversation, use earlier same-day results as optional but important context. Compare the new result with the earlier answer when migration could change the judgment, when the user asks "now/again", or when spot is near a wall, pit, flip, or trigger: spot, net GEX, net VEX, flip, nearest wall, nearest pit, CPR relationship, and rough magnet/bias if calculated. State what migrated and what strengthened/weakened. If a prior JSON snapshot exists or the user provides one, run `spx_intraday_latest.py --compare-json ...`; if the user asks about a specific level such as `7400支撑还在吗`, include it in `--watch-strikes`. Always check whether the same strike's GEX sign or magnitude changed materially across 0DTE, Next2, Fri2w, and All buckets, but do not mechanically dump same-strike change rows in the final answer. Translate the comparison into what it means and what it may foreshadow: support quality deteriorating or recovering, risk center migrating lower/higher, upper pinning weakening, reflexive selling/buying risk rising, or chop/pinning returning. Treat positive-to-negative GEX migration at an active battlefield strike as `支撑跑路/降级为加速风险`, not merely as a lower wall ranking. Treat negative-to-positive migration as `支撑恢复/加速风险缓和`, but still require price action to confirm. If no earlier same-day result exists in the conversation or user-provided notes, do not imply there is an internal time series.

## Dark Pool / Short Data Layer

Use this layer only for U.S.-listed stocks and ETFs. Do not apply it to A-shares, Japanese stocks, or non-U.S. local listings.

When using ChartExchange, build the URL from both listing venue and ticker. The path shape is:

```text
https://chartexchange.com/symbol/{exchange-lowercase}-{ticker-lowercase}/exchange-volume/dark-pool-levels/
```

Examples: `nyse-anet`, `nasdaq-nvda`, `nyse-spy`. SPY is a common exception where ChartExchange uses `nyse-spy`, so search the ticker on ChartExchange or a quote source first when the venue is uncertain, then use the matching venue in the URL. Do not reuse an ANET URL for other tickers without changing both ticker and venue.

Interpretation rules:

- `Off Exchange & Dark Pool %`: compare today's share with the ticker's own average. A high off-exchange share is common in U.S. equities and is not bullish or bearish by itself.
- `Dark Pool Levels`: treat high-volume price levels as hidden-liquidity reference zones. They become support/resistance only if later price action confirms acceptance, rejection, or repeated defense.
- `Dark Pool Prints`: large prints near VWAP, gaps, prior highs/lows, or post-news levels are notable, but the data does not reveal whether the initiating side was accumulation, distribution, internalization, or a cross.
- `Short Volume`: daily short-sale volume is not short interest and often includes market-maker activity. Use it for flow pressure only, not for outstanding short exposure.
- `Short Interest`, `Borrow Fee`, `Shares Available`, and `FTD`: use these for squeeze risk. Stronger squeeze evidence is rising borrow fee, shrinking availability, elevated short interest/FTD, and price refusing to break down after heavy short/dark flow.
- Always combine this layer with news acceptance, live price/VWAP, volume, and option/gamma structure. If the conclusion depends on a dark-pool level becoming support/resistance, load `stock-technical-analysis` and require price confirmation.

## Optional User Knowledge Base

Do not read local research folders by default. If a user wants to incorporate their own study materials, ask them to specify a private RAG or index folder outside this public repository:

- keep raw PDFs, screenshots, notes, and proprietary indicators in a private local folder or private vector store;
- offer to create or update a lightweight local index for repeated use, with only user-approved aliases, topics, page/slide ranges, keywords, and public-safe summaries;
- extract only reusable, public-safe rules into this skill when the user explicitly asks to update the skill;
- strip private paths, account details, ticker-specific trade logs, original strategy names, private person names/handles, unique document labels, and memorable private labels;
- keep this skill functional even when that private RAG corpus is unavailable.

## Required Interpretation Style

Write like a pre-market trading memo:

1. **一句话**: where the stock is now and whether it is near a wall, support, or flip.
2. **我会怎么做**: concrete scenario handling, e.g. “do not chase until it holds X”, “treat X-Y as chop”, “above Z opens next target”.
3. **什么情况说明我错了**: exact invalidation levels.
4. **怎么和技术确认配合**: use gamma as the map, then confirm entries/exits with `stock-technical-analysis` concepts such as KDJ, MACD, MA144/Vegas, FVG, volume, and price action.

Avoid only dumping tables. The user wants judgment, assumptions, and a clear action framework.

When news or broad risk sentiment is driving the underlying or index, call `macro-news-check` only when current macro tape can plausibly change the gamma read, such as CPI/PCE/FOMC/central-bank events, Treasury yield shocks, USD moves, oil/gold/geopolitical headlines, index futures breaks, or sudden risk-on/risk-off tape. Use `stock-sentiment-analysis` if deeper emotion-cycle framing is needed, and add an expectation-gap check before relying on the gamma map: `prior market expectation` -> `actual news` -> `above expectation / in line or merely landed / below expectation`. Apply this to numeric headlines such as orders, CPI/FOMC data, earnings, guidance, and ETF flows, and to qualitative headlines such as regulatory wording, geopolitical tone, management confidence, timing, certainty, and whether the news solves the market's real concern. Gamma explains likely hedging pressure after price moves; it does not by itself explain whether the headline was accepted or rejected.

## Gamma Reading Rules

- `gamma wall`: a price where positive GEX is concentrated; price often slows, pins, or rejects there.
- `gamma flip`: estimated transition between positive and negative gamma regimes.
- `vanna`: estimated change in option delta as IV changes. Moomoo usually provides enough inputs to compute it even when it does not provide a direct `option_vanna` field.
- `VEX`: aggregate vanna exposure by strike. Use it to identify where IV crush/IV expansion can force meaningful delta adjustment; do not treat it as a standalone direction signal.
- Positive gamma: more chop/pinning/mean-reversion; avoid chasing into walls without confirmation.
- Negative gamma: more trend amplification; be quicker with stops and avoid casual dip-buying.
- Low-gamma trough: path of least resistance; price may move faster through it.
- Vanna pressure matters most around macro/news vol crushes, 0DTE IV resets, and strong spot moves that also reprice IV. Report the top positive and negative vanna zones alongside gamma walls.

## SPX, SPY, And ES Point Conversion

When analyzing SPX with proxy instruments, never hard-code a fixed 10x conversion:

- Prefer `.SPX` option chains from moomoo as `US..SPX` when available. Moomoo may reject the SPX index snapshot while still allowing SPX/SPXW option expiries and chains.
- Do not assume OpenD can provide `US..SPX` real-time 1-minute K-lines. Some OpenD setups return `暂不支持美股指数` for `US..SPX` `SubType.K_1M` / `get_cur_kline`. For SPX intraday price-action confirmation, use `US.SPY` 1-minute K-lines as the chart proxy: reuse the existing `US.SPY` `SubType.K_1M` subscription when it is still valid; if K-line retrieval says subscription is missing or stale, subscribe/re-subscribe and retry once. Then convert the relevant SPY prices to SPX-equivalent levels with the freshest SPX/SPXW parity anchor or live ES/SPX anchor. State that SPY is the K-line source.
- Treat user requests for `SPX`, `SP500`, `S&P 500`, or `标普500` gamma as SPX-index-option requests by default. Query `US..SPX` expiries/chains first and use the returned SPX/SPXW strikes directly; do not default to SPY options just because the SPX index snapshot is unavailable.
- When `US..SPX` chains are available, do not use SPY conversion for SPX/SP500 gamma. SPY/ES/CFD conversion is only a fallback when the SPX/SPXW chain is unavailable, permission-blocked, or user-provided data is explicitly proxy-based.
- For same-day intraday/0DTE gamma, prefer PM-settled `SPXW` contracts from the `US..SPX` chain. On dates that also list AM-settled monthly `SPX` contracts, exclude the AM-settled series from the intraday pin/gamma map unless the user specifically asks about AM settlement.
- Use live SPX/ES/CFD price as the spot anchor for index levels, then use SPX option strikes directly whenever possible.
- If using SPY options as a proxy, compute the same-day conversion ratio from simultaneous prices: `SPX_equiv = SPY_strike * (current_SPX_or_ES_anchor / current_SPY_price)`.
- If using ES as the price anchor, remember ES can trade at a futures basis versus SPX cash. State the anchor and basis explicitly, e.g. “SPY 734 with ES/SPX anchor 7355 implies ratio about 10.02 today.”
- If live SPX/ES is unavailable, an external SPX/SPY ratio such as prior close from Yahoo Finance, Investing.com, Barchart, or another current quote source can be used as an approximate fallback. Clearly state the source/time and that it is not a live simultaneous conversion.
- Recompute the ratio every session and after large moves; do not carry yesterday's ratio into today's levels.

## Nikkei / EWJ Proxy Conversion

- Treat `Nikkei`, `日经`, `日経`, `NKY`, `Nikkei 225`, and `日经225` gamma requests as index-proxy work, not a plain EWJ ETF gamma request.
- Use `US.EWJ` options as the proxy book only because moomoo may not provide the domestic Nikkei option chain. The conversion must be time-aligned:
  `Nikkei_equiv = EWJ_strike * (NKD_at_EWJ_quote_time / EWJ_quote_spot) * (current_NIY_or_CFD_anchor / current_NKD)`.
- Prefer `NKDmain` as the bridge because it is the USD Nikkei futures line closer to the US/EWJ session. Use `NIYmain` or the user's Nikkei CFD/index quote as the final current anchor when available.
- If EWJ has already closed, do not pair its closing price with the current Nikkei CFD directly. Use the Nikkei futures/CFD value at EWJ's quote timestamp to form the EWJ-to-NKD ratio, then bridge from current NKD to current NIY/CFD.
- If using Japan cash close as the anchor, pair it only with an EWJ overnight/24h quote from the same timestamp. If no real EWJ quote exists at Japan close, do not mix Japan cash close with the later US regular-session EWJ close.
- Moomoo may recognize `US.NKDmain` and `US.NIYmain` but return permission errors. If that happens, ask the user for: `NKD at EWJ close/update time`, `current NKD`, and `current NIY or Nikkei CFD`.
- User fallback formula when better anchors are unavailable: `Nikkei target = 62038 * EWJ target / 91.265`. Treat this as a rough stored fallback, not the preferred method. Each time, first decide whether current NKD/NIY/EWJ time-aligned anchors can improve it; if not, use this formula and label it as the fallback conversion.
- Do not carry a prior EWJ/Nikkei ratio into a new session. Recompute after large FX, futures, or EWJ moves.
- In the writeup, list both the converted Nikkei levels and the source EWJ strikes for auditability.
- State the limitation: EWJ options capture US-listed Japan ETF positioning, USD/JPY and ETF-flow effects; they are not the full domestic Nikkei options dealer book.

## Option Expiry Selection

Use a broader but still relevant option window instead of blindly taking the first few expiries. Keep horizons clean instead of mixing daily, weekly, and monthly expiries:

- **0DTE / expiry day**: when the user asks about an expiry-day gamma pin, analyze the same-day expiry as its own bucket.
- **Next 2 trading days**: for high-frequency option tickers, include the next 2 listed trading-day/daily expiries after today. Do not include today in this bucket when 0DTE is already shown separately.
- **Future 2 weeks weekly options**: include only Friday expiries after today within the next 14 calendar days. Do not mix Monday-Thursday daily expiries into this weekly bucket.
- **Future monthly options**: include only standard monthly expiries for the current month and next 2 months, and only include the current month if it has not passed and is not already being handled as the same-day 0DTE bucket.
- **High-frequency option tickers**: examples include broad index ETFs and very liquid single names such as `SPY`, `QQQ`, `IWM`, `DIA`, `TSLA`, `NVDA`, `AMD`, `AAPL`, `MSFT`, `AMZN`, `META`, `GOOGL`, `PLTR`.
- In the writeup, mention when the ticker only has monthly expiries or when the near-term weekly/daily window is unavailable.

## Moomoo Data Caveats

- Do not remove option-chain throttling from scripts. OpenD can return `获取期权链频率太高，请求失败，每30秒最多10次`; reusable fixes for that limit belong in `scripts/gamma_report.py`, not only in one-off project scripts.
- During US pre-market, stock fields such as `pre_price`, `pre_high_price`, `pre_low_price`, and `pre_volume` may update, but listed options usually do not trade continuously. Greeks/IV/OI may still reflect the prior option session.
- Open interest is not real-time intraday dealer inventory. `option_net_open_interest` may be empty.
- GEX sign is a market convention, not proof of actual market-maker net positions.
- Re-run after the regular session opens if option volume or the stock price moves materially.

## Data Safety

- This is analysis, not a trade instruction.
- Do not place trades unless the user explicitly asks and confirms.
- Never call SDK trade unlock APIs. If trading unlock is needed, the user must do it manually in the OpenD GUI.

## When Chat-Only Is Enough

If the user asks for a quick look, run the relevant script and answer from its text output. Do not link a report or attach a file unless the user explicitly requested one.
