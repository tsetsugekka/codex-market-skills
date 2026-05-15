---
name: us-stock-gamma-moomoo
description: Analyze US stock and ETF option gamma exposure with moomoo OpenD, plus .SPX/SPXW index-option structure using SPY/ES/CFD conversion when needed. Use when the user asks for gamma, GEX, gamma wall, gamma flip, SPX/SPY/ES intraday gamma, 0DTE option scenario value tables, option positioning, or a web report. Produces plain-language conclusions plus a local HTML report using moomoo option chain, snapshots, Greeks, OI, IV, and pre-market/latest stock price.
metadata:
  version: 0.1.3
---

# US Stock Gamma With moomoo

Use this skill to turn moomoo OpenD option data into an actionable gamma map and a plain-language trading note.

This public-safe skill is self-contained. Do not commit personal information, API keys, account data, private RAG files, or any `Stocks` folder contents to GitHub. It may use a user-specified private RAG folder during a session, but it must not store private source paths, personal positions, original strategy names, private person names/handles, proprietary labels, or private document titles. Generic market concepts such as gamma, GEX, dealer hedging, FVG, KDJ, MACD, RSI, VWAP, and Vegas may be retained.


## Public And Private Versions

If both public and private versions of this skill exist, prefer the private version for local analysis when the user permits it. The private version may use local RAG indexes and user-specific study material.

When updating the skill, keep public and private versions in sync: write public-safe, generalized lessons to the public version; keep private labels, private paths, raw notes, screenshots, account data, and personal trade context only in the private version or private RAG index.

When preparing a GitHub upload or public release, use the public version only and run the release/privacy check in `stock-sentiment-analysis/references/release-and-privacy.md`. Never upload `Stocks/`, private RAG folders, `.ftindex` files, credentials, `.env`, personal data, screenshots, raw PDFs/PPTs, or private strategy labels.

## Experience

Before deep analysis, read `references/experience.md` if it exists, but only `Active Playbook` and `Compression Protocol` unless the user explicitly asks for historical lessons. If a multi-turn correction produces a durable reusable lesson about gamma interpretation, option scenario handling, news/gamma interaction, or chart confirmation, update that file after answering. Generalize the lesson and strip private details.

## Environment Check

This skill requires moomoo OpenD plus the Python SDK/skills environment.

- First check whether OpenD is running and the `moomoo` Python package imports. If not, guide the user to install or launch OpenD using the `install-moomoo-opend` skill.
- Tell the user OpenD must stay running in the background while querying quotes/options. Login may be required for permissioned data.
- Do not ask the user to unlock trading or input an encrypted private key unless they explicitly want trading functions. This skill only needs quote/option data.
- If moomoo cannot provide a live index snapshot, use available option chains plus a user-provided/live SPX, ES, CFD, or SPY anchor and state the anchor clearly.

## Default Output

Prefer a local HTML report, not just chat text. Use `scripts/gamma_report.py`:

```bash
python3 ~/.codex/skills/us-stock-gamma-moomoo/scripts/gamma_report.py US.BA
python3 ~/.codex/skills/us-stock-gamma-moomoo/scripts/gamma_report.py US.MP --output /path/to/report.html
```

The script:
- reads stock snapshot, option expirations, option chain, option snapshots, and daily K lines from moomoo OpenD;
- uses `pre_price` when available, otherwise bid/ask midpoint, otherwise regular-session last price;
- gathers option `OI`, `IV`, `delta`, `gamma`, `theta`, `vega`, bid/ask, volume;
- selects option expiries by default as: all weeklies within the next 2 calendar weeks when available, plus monthly expiries for the current month and next 2 months; for high-frequency option names also include the next 2 trading-day/daily expiries when listed;
- calculates signed GEX with the common assumption `Call = +`, `Put = -`;
- recomputes gamma across a spot-price grid to estimate gamma wall, gamma trough, and gamma flip;
- writes a local HTML report with conclusions first and charts second.

For SPX 0DTE or quick trading questions, chat-only is acceptable when a report would slow the answer. Still compute or fetch the chain first when possible.

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

When news or broad risk sentiment is driving the underlying or index, use `stock-sentiment-analysis` if needed and add an expectation-gap check before relying on the gamma map: `prior market expectation` -> `actual news` -> `above expectation / in line or merely landed / below expectation`. Apply this to numeric headlines such as orders, CPI/FOMC data, earnings, guidance, and ETF flows, and to qualitative headlines such as regulatory wording, geopolitical tone, management confidence, timing, certainty, and whether the news solves the market's real concern. Gamma explains likely hedging pressure after price moves; it does not by itself explain whether the headline was accepted or rejected.

## Gamma Reading Rules

- `gamma wall`: a price where positive GEX is concentrated; price often slows, pins, or rejects there.
- `gamma flip`: estimated transition between positive and negative gamma regimes.
- Positive gamma: more chop/pinning/mean-reversion; avoid chasing into walls without confirmation.
- Negative gamma: more trend amplification; be quicker with stops and avoid casual dip-buying.
- Low-gamma trough: path of least resistance; price may move faster through it.

## SPX, SPY, And ES Point Conversion

When analyzing SPX with proxy instruments, never hard-code a fixed 10x conversion:

- Prefer `.SPX` option chains from moomoo as `US..SPX` when available. Moomoo may reject the SPX index snapshot while still allowing SPX/SPXW option expiries and chains.
- Use live SPX/ES/CFD price as the spot anchor for index levels, then use SPX option strikes directly whenever possible.
- If using SPY options as a proxy, compute the same-day conversion ratio from simultaneous prices: `SPX_equiv = SPY_strike * (current_SPX_or_ES_anchor / current_SPY_price)`.
- If using ES as the price anchor, remember ES can trade at a futures basis versus SPX cash. State the anchor and basis explicitly, e.g. “SPY 734 with ES/SPX anchor 7355 implies ratio about 10.02 today.”
- Recompute the ratio every session and after large moves; do not carry yesterday's ratio into today's levels.

## Option Expiry Selection

Use a broader but still relevant option window instead of blindly taking the first few expiries:

- **Future 2 weeks**: include listed weekly expiries within the next 14 calendar days when they exist. If the ticker has no weeklies, do not invent a substitute.
- **Future 3 months monthly options**: include monthly expiries for the current month and the next 2 months. Include the current month only when that monthly expiry has not passed.
- **High-frequency option tickers**: for very active names with daily/near-daily expiries, also include the next 2 trading-day/daily expiries when listed. Examples include broad index ETFs and very liquid single names such as `SPY`, `QQQ`, `IWM`, `DIA`, `TSLA`, `NVDA`, `AMD`, `AAPL`, `MSFT`, `AMZN`, `META`, `GOOGL`, `PLTR`.
- In the writeup, mention when the ticker only has monthly expiries or when the near-term weekly/daily window is unavailable.

## Moomoo Data Caveats

- During US pre-market, stock fields such as `pre_price`, `pre_high_price`, `pre_low_price`, and `pre_volume` may update, but listed options usually do not trade continuously. Greeks/IV/OI may still reflect the prior option session.
- Open interest is not real-time intraday dealer inventory. `option_net_open_interest` may be empty.
- GEX sign is a market convention, not proof of actual market-maker net positions.
- Re-run after the regular session opens if option volume or the stock price moves materially.

## Data Safety

- This is analysis, not a trade instruction.
- Do not place trades unless the user explicitly asks and confirms.
- Never call SDK trade unlock APIs. If trading unlock is needed, the user must do it manually in the OpenD GUI.

## When Chat-Only Is Enough

If the user asks for a quick look, still prefer running the report script first, then summarize the HTML's “一句话 / 我会怎么做 / invalidation” sections in chat and link the report.
