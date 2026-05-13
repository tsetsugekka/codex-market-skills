# SPX Intraday Gamma Reference

Use this only for `.SPX`, `SPXW`, `SPY`, `ES`, SpotGamma/TRACE heatmaps, or intraday index judgment.

## Analysis Order

1. **Anchor**: current SPX cash when available; otherwise ES/CFD anchor with basis disclosed; SPY only as a converted proxy.
2. **0DTE structure**: net GEX, call/put volume balance, largest positive walls above, largest negative pits below, and gamma flip if meaningful.
3. **Opening context**: distinguish prior close, current price, and same-day open. If the user says the market gapped down, do not treat prior close as the open.
4. **Key level map**: name nearby support/resistance as zones, not single magic points. Example: "7350 is the battlefield; 7330/7300 are next downside magnets; 7385-7415 is repair/sell-pressure."
5. **Flow interpretation**: in negative gamma, breaks can accelerate and rebounds can be violent short-covering. Do not call a bottom merely because price is near a put wall.
6. **Invalidation**: state what would disprove the scenario, e.g. "reclaiming 7370 and holding above it makes 7385-7390 likely; losing 7350 and failing to reclaim opens 7330/7300."

## SPY/ES Conversion

- Prefer `.SPX` option chains from moomoo as `US..SPX` when available.
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
