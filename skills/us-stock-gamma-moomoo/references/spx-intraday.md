# SPX Intraday Gamma Reference

Use this only for `.SPX`, `SPXW`, `SPY`, `ES`, SpotGamma/TRACE heatmaps, or intraday index judgment.

## Analysis Order

1. **Anchor**: current SPX cash when available from a live source. If moomoo rejects the SPX index snapshot but `US..SPX` 0DTE chains are available, infer the intraday anchor from liquid SPXW put-call parity (`spot/forward ~= strike + call_mid - put_mid`) using same-expiry PM-settled pairs near the market. Do not use delayed/static TradingView page text as the intraday anchor unless a live chart value is explicitly confirmed. SPY is only a sanity check or last-resort proxy.
2. **0DTE structure**: net GEX, call/put volume balance, largest positive walls above, largest negative pits below, and gamma flip if meaningful.
3. **Vanna structure**: compute vanna from SPXW spot/strike/IV/DTE, aggregate VEX by strike, and name the top positive/negative vanna pressure zones. This is required when the user asks for SPX/SP500 gamma unless speed is explicitly more important than completeness.
4. **Opening context**: distinguish prior close, current price, and same-day open. If the user says the market gapped down, do not treat prior close as the open.
5. **Key level map**: name nearby support/resistance as zones, not single magic points. Example: "7350 is the battlefield; 7330/7300 are next downside magnets; 7385-7415 is repair/sell-pressure."
6. **Flow interpretation**: in negative gamma, breaks can accelerate and rebounds can be violent short-covering. Do not call a bottom merely because price is near a put wall.
7. **Invalidation**: state what would disprove the scenario, e.g. "reclaiming 7370 and holding above it makes 7385-7390 likely; losing 7350 and failing to reclaim opens 7330/7300."

## Vanna Calculation

- Moomoo may not expose `option_vanna`, but SPXW snapshots usually include the required inputs: spot anchor, strike, IV, DTE, OI, and contract size.
- Use Black-Scholes vanna: `vanna = -normal_pdf(d1) * d2 / iv`, where `d2 = d1 - iv * sqrt(T)`. This is delta change per 1.00 vol unit; multiply by `0.01` for one IV point.
- Aggregate signed VEX by strike as `sign * vanna * 0.01 * OI * 100 * spot`, using the same explicit convention as GEX (`Call = +`, `Put = -`) and labeling it as an assumption.
- Interpret vanna together with IV direction: after an IV crush, large vanna zones can drive delta adjustments; during IV expansion, the pressure can reverse. Gamma still controls immediate pin/acceleration zones.

## SPY/ES Conversion

- Prefer `.SPX` option chains from moomoo as `US..SPX` when available. Moomoo can reject `get_market_snapshot(["US..SPX"])` with an unsupported-index error while still returning `get_option_expiration_date("US..SPX")` and `get_option_chain("US..SPX")`.
- Treat `SPX`, `SP500`, `S&P 500`, and `标普500` gamma requests as direct SPX-index-option work first. Use SPX/SPXW strikes directly; use SPY/ES conversion only when the SPX option chain itself is unavailable or permission-blocked.
- If `US..SPX` chains are available, skip SPY conversion entirely for gamma levels; SPY is only a proxy fallback, not the normal SPX workflow.
- For 0DTE intraday gamma, prefer PM-settled `SPXW` contracts. If the same date includes AM-settled monthly `SPX` contracts, exclude those AM contracts from the intraday pin/gamma map unless the user explicitly asks about AM settlement.
- When live SPX cash is unavailable, estimate the anchor from liquid same-day SPXW pairs with put-call parity. Prefer multiple near-ATM strikes with tight bid/ask and meaningful volume/OI, then use a weighted median or trimmed weighted mean. State this as a parity-implied SPX/forward anchor.
- Do not use cached or delayed TradingView page text as the intraday anchor. If TradingView is mentioned, assume it is stale unless the value is explicitly confirmed from a live chart/front-end tick.
- If using SPY options as a proxy, compute the same-day conversion ratio from simultaneous prices: `SPX_equiv = SPY_strike * (current_SPX_or_ES_anchor / current_SPY_price)`.
- If using ES, state the futures basis explicitly. Do not carry yesterday's ratio into today.
- If moomoo cannot provide ES due to permissions, accept user-provided ES/CFD screenshots as the anchor and disclose that limitation.

## SpotGamma/TRACE Heatmap Reading

- A blue/projection line moving before price is a proprietary gamma/hedging contour, not the traded SPX price. It can warn that options structure deteriorated before spot moved, but do not try to reproduce it exactly.
- `SG Implied 1d Move High/Low` is an implied statistical range, not a gap. "Filling a gap" and "touching implied low" are different ideas.
- A `Call Wall` is usually resistance/pin unless reclaimed; a `Hedge Wall`/large downside put pit can attract price in negative gamma but may also create reflexive rebounds.

## Practical Judgment

- In negative gamma, do not over-trust a single support line. Require reclaim/hold behavior.
- Strong relief rallies can happen after "not worse than feared" macro events when dealers and shorts are already leaning downside.
- For gap-down days, separate "rebound to open" from "rebound to prior close"; these are different targets and probabilities.
- Phrase conclusions probabilistically: "a bounce attempt is more likely than clean continuation if 7350 keeps holding," not "it must rebound."
