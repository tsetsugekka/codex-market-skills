# Option Scenario Tables Reference

Use this when the user owns or asks about a specific short-dated option, especially SPXW 0DTE.

## Required Inputs

- Option code, strike, call/put, expiry.
- Current option bid, ask, last, IV, delta, gamma, theta, vega if available.
- Current underlying anchor. For SPXW, prefer SPX cash; otherwise use ES/CFD/SPY conversion and disclose it.
- User's option cost and contract count when they ask about break-even or recovery.

## Table Rules

- Build a scenario table with time on the horizontal axis and underlying price on the vertical axis.
- Use Japan time for this user unless they request another timezone.
- Use 30-minute steps for 0DTE during the final 4 hours; use 1-hour steps when farther from expiry.
- Price with Black-Scholes using the current IV as the base case.
- Include intrinsic value at expiry so the user sees where the option goes to zero and where it becomes pure intrinsic.
- Warn that IV crush/expansion and bid-ask slippage can make real fills worse or better.

Use `scripts/option_scenario_table.py`:

```bash
python3 ~/.codex/skills/us-stock-gamma-moomoo/scripts/option_scenario_table.py \
  --kind C --strike 7370 --iv 16.8 \
  --asof 2026-05-13T02:30:00+09:00 --expiry 2026-05-13T05:00:00+09:00 \
  --spots 7350,7360,7370,7380,7390
```

## Interpreting Calls

- Below strike: theta decay dominates unless price moves fast.
- Near strike: gamma is high, price can double or halve quickly.
- Above strike: intrinsic value dominates, but a pullback below strike can erase premium late in the day.

## Interpreting Puts

- Above strike: theta decay dominates unless price falls fast.
- Near strike: gamma is high and risk changes quickly.
- Below strike: intrinsic value dominates, but a rebound above strike can erase premium late in the day.

## Recovery Math

- Do not expose the user's account size or deposit/transfer amount.
- Translate recovery into option price points. For SPX options, 1.00 option point is usually `$100` per contract before FX/fees.
- Example wording: "with 2 contracts, every 1.00 option point is about $200 before FX/fees; to recover X JPY at USDJPY Y, the option needs about Z points more."
- Use the table for decision framing: "needs SPX to reach 7380 before 03:00 JST" is actionable; "will profit" is too strong.
