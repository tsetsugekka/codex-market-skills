# US Stock Gamma Experience

## Active Playbook

- Read gamma as a positioning map, not a standalone forecast. Confirm the map with live spot, price action, volatility, and news acceptance.
- Before leaning on GEX after a headline, run an expectation-gap check: what was priced, what landed, and whether price accepted or rejected it.
- Use `stock-technical-analysis` when entry/exit timing, 1h+ structure, support/resistance, or failed-breakout confirmation matters.
- Use `stock-sentiment-analysis` when rates, FX, volatility, crowded AI/semiconductor positioning, or broad risk-on/risk-off behavior is driving the underlying.
- For SPX/SP500 gamma, try `US..SPX` option expiries/chains first even if the SPX index snapshot fails. When that chain is available, do not use SPY conversion; use SPX/SPXW strikes directly. Use SPXW PM-settled contracts for same-day intraday/0DTE maps and filter out AM-settled monthly SPX unless AM settlement is the question.
- De-duplicate moomoo SPX expiry dates before fetching chains. On monthly-expiry Fridays, `get_option_expiration_date("US..SPX")` can return the same `strike_time` twice for `MONTH` and `WEEK`; fetching both rows by date double-counts the same chain and inflates GEX/VEX.
- For intraday SPX spot anchoring, prefer SPXW 0DTE put-call parity from the same moomoo option chain when the OpenD SPX index snapshot is unavailable. Do not use delayed/static TradingView page text as an anchor; ignore it unless a live chart value is explicitly confirmed. SPY is a sanity check, not the normal anchor.
- For intraday questions such as "now", "today", "can it get through", or "0DTE", make the same-day SPXW bucket the primary read. Use `Next2`, `Fri2w`, and `All` only as background unless the user asks about the week.
- If comparing with a third-party gamma dashboard, do not claim to reproduce proprietary `flip`, `magnet`, `pressure`, `bias`, or `trigger` values. Label local outputs as self-calculated from SPXW option chains, and keep third-party levels separate when the user provides them.
- For intraday SPX output, include ladders rather than a single level: call-OI walls, put-OI walls, positive-GEX gamma walls, negative-GEX gamma pits, and major vanna zones. Put walls and gamma pits are different: put-OI walls can act as defense/support, while negative-GEX pits are volatility/acceleration zones.
- Do not treat the first touch or brief break of a gamma pit as an automatic short signal. If a put wall and pit overlap, call it a battlefield; require failure to reclaim, loss of the next nearby pit/trigger, or price-action confirmation before describing downside continuation.
- When an option/gamma answer uses macro/flash-news, technical, or sentiment reasoning, call the corresponding sibling skill instead of folding that layer into this skill ad hoc: `macro-news-check` for 宏观/快讯, `stock-technical-analysis` for 技术面, and `stock-sentiment-analysis` for 情绪面/期待差. State the fusion layers in the final answer when they materially affect the conclusion.
- For SPX/SP500 reports, calculate vanna from SPXW spot/strike/IV/DTE and analyze top positive/negative VEX zones alongside gamma walls. Treat VEX as an IV-sensitive pressure map, not a standalone forecast.
- Keep SPX report render helpers compatible with both per-level pairs and scalar level lists. `flips` are scalar floats, while walls/pits are `[level, value]` pairs; text rendering must not assume every level list is two-dimensional.
- When writing index ranges, support/resistance, walls, pits, triggers, or scenario levels, list prices from high to low so the map reads top-down.
- Throttle sequential `get_option_chain` calls in reusable scripts and retry once after OpenD frequency-limit errors. If a project-specific script adds this workaround, port the same behavior back to `us-stock-gamma-moomoo/scripts/gamma_report.py` and the installed skill; otherwise the next ticker or ETF report can hit the same 10-requests-per-30-seconds limit again.
- Keep index-specific algorithms as first-class skill scripts, not project-local scratch scripts. SPX/SPXW should route to `scripts/spx_intraday_latest.py`; Nikkei index work should route through `scripts/proxy_index_gamma.py` using EWJ options converted through a time-aligned `EWJ -> NKDmain -> NIYmain/current CFD` bridge. Generic `gamma_report.py` is for ordinary US stocks/ETFs and can be an input check, not the final answer for those index workflows.
- For Nikkei proxy conversion, never pair a stale EWJ close with the current Nikkei CFD directly. If EWJ is closed, anchor the EWJ/NKD ratio using NKDmain or Nikkei CFD at the EWJ quote timestamp, then bridge to current NIYmain/current CFD with a current NKD/NIY ratio. If moomoo returns permission errors for `US.NKDmain` or `US.NIYmain`, ask for those anchors explicitly.
- If a Nikkei cash close anchor is used, it must pair with an EWJ overnight/24h quote at the same Japan-close timestamp. Do not pair Japan cash close with the later US regular-session EWJ close.
- If no better time-aligned Nikkei anchors are available, use the user's stored fallback conversion: `Nikkei target = 62038 * EWJ target / 91.265`. Before using it, check whether current NKD/NIY/EWJ anchors can replace it; if not, label it as an approximate fallback and list source EWJ strikes.
- For SPX/Nikkei special workflows, default to a concise human text summary. Do not generate JSON, HTML, or any other file unless the user explicitly requests a raw export or report artifact; unfinished files should not appear as incidental artifacts.
- Re-run after the regular session opens or after a large spot move; pre-market stock moves often use stale option IV/OI/Greeks.

## Compression Protocol

- Always read only `Active Playbook` first.
- Merge repeated lessons instead of appending duplicates.
- Keep this section compact and public-safe. Do not store private paths, account data, original strategy names, personal labels, or ticker-specific private trade logs.

## Conversation Learning Protocol

- Update this file only when a multi-turn correction reveals a reusable gamma lesson: expiry selection, stale Greeks, SPX/SPY/ES conversion, news/gamma interaction, or chart confirmation.
- If the lesson is mostly sentiment-related, update `stock-sentiment-analysis/references/experience.md` instead or as well.

## Archive

- 2026-05-15: Added initial public-safe gamma experience protocol.
- 2026-05-15: Added SPX expiry de-duplication rule after a monthly-expiry Friday produced duplicate `MONTH`/`WEEK` rows for the same date and inflated 0DTE GEX/VEX.
- 2026-05-16: Added output-format rule to list price levels from high to low.
- 2026-05-17: Added OpenD option-chain throttling/sync rule after a project-specific SPY script had a frequency-limit workaround that had not been propagated to the reusable gamma report script.
- 2026-05-17: Promoted SPX/SPXW parity-anchor and Nikkei EWJ-to-CFD proxy workflows into explicit skill routing so index requests do not silently fall back to the generic ETF gamma report.
- 2026-05-17: Refined Nikkei proxy conversion to use time alignment: EWJ quote-time price must pair with NKDmain/Nikkei futures at the same timestamp, then bridge to current NIYmain/current CFD. Direct current CFD divided by stale EWJ close is invalid unless the timestamps match.
- 2026-05-17: Added user fallback ratio for Nikkei proxy work: `62038 / 91.265`, to use only when better EWJ/NKD/NIY time-aligned anchors are unavailable.
- 2026-05-18: Changed gamma workflows to default to text-only output. HTML and JSON are explicit opt-in artifacts, not default side effects.
- 2026-05-19: Added intraday SPX lesson to separate self-calculated SPXW gamma maps from proprietary dashboard flip/magnet/pressure values, and to report call/put OI walls separately from gamma walls/pits.
- 2026-05-19: Added mandatory fusion rule: macro/flash-news, technical, and sentiment layers must route to their sibling skills when used.
- 2026-05-21: Fixed SPX intraday text rendering after `flips` returned scalar floats while `levels()` expected `[level, value]` pairs.
