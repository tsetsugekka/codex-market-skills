# US Stock Gamma Experience

## Active Playbook

- Read gamma as a positioning map, not a standalone forecast. Confirm the map with live spot, price action, volatility, and news acceptance.
- Before leaning on GEX after a headline, run an expectation-gap check: what was priced, what landed, and whether price accepted or rejected it.
- Use `stock-technical-analysis` when entry/exit timing, 1h+ structure, support/resistance, or failed-breakout confirmation matters.
- Use `stock-sentiment-analysis` when rates, FX, volatility, crowded AI/semiconductor positioning, or broad risk-on/risk-off behavior is driving the underlying.
- For SPX/SP500 gamma, try `US..SPX` option expiries/chains first even if the SPX index snapshot fails. When that chain is available, do not use SPY conversion; use SPX/SPXW strikes directly. Use SPXW PM-settled contracts for same-day intraday/0DTE maps and filter out AM-settled monthly SPX unless AM settlement is the question.
- De-duplicate moomoo SPX expiry dates before fetching chains. On monthly-expiry Fridays, `get_option_expiration_date("US..SPX")` can return the same `strike_time` twice for `MONTH` and `WEEK`; fetching both rows by date double-counts the same chain and inflates GEX/VEX.
- For intraday SPX spot anchoring, prefer SPXW 0DTE put-call parity from the same moomoo option chain when the OpenD SPX index snapshot is unavailable. Do not use delayed/static TradingView page text as an anchor; ignore it unless a live chart value is explicitly confirmed. SPY is a sanity check, not the normal anchor.
- For SPX/SP500 reports, calculate vanna from SPXW spot/strike/IV/DTE and analyze top positive/negative VEX zones alongside gamma walls. Treat VEX as an IV-sensitive pressure map, not a standalone forecast.
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
