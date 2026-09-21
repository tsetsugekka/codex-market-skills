# SPX Gamma Heatmap Visualization

Use this reference when the user asks for a chart similar to a multi-expiry gamma surface, wants the current chart refreshed, or asks for smoother heatmap rendering.

## Chart Semantics

- Horizontal axis: real listed SPX/SPXW expiries in the verified option-chain input. Never invent a missing daily expiry.
- Vertical axis: SPX strike levels, normally using the native 5-point spacing near spot.
- Heatmap color: signed GEX by strike for each expiry at the current SPX pricing anchor.
- Left profile: all-selected-expiry Call GEX mirrored right of zero and absolute Put GEX mirrored left of zero on a single shared scale. Overlay the raw Net GEX as a thin line. Do not render the Net GEX as a separate bar.
- Solid line: each expiry's self-calculated gamma flip. This is a regime boundary, not a predicted SPX path.
- Dashed line: current SPX pricing anchor.
- Call-wall line: the `call_wall.level` calculated only from that expiry's contracts, meaning the strike with the largest call-side GEX at the current anchor.
- Put-wall line: the `put_wall.level` calculated only from that expiry's contracts, meaning the strike with the most negative put-side GEX at the current anchor. It is not automatic support after price loses it.
- Use accessible positive/negative colors appropriate to the actual output host.

This chart is a transparent, self-calculated option-chain view. Do not claim that it reproduces a proprietary vendor's forward gamma model.

## Range And Granularity

- Honor a user-specified range exactly when the option-chain data covers it.
- If no range is supplied, use `floor(spot / 100) * 100 - 300` to `ceil(spot / 100) * 100 + 300`. An anchor of 7480 therefore renders 7100-7800. Do not retain a fixed 7000-7700 default.
- Do not replace native 5-point strikes with 25-point buckets merely to reduce row count. Broad negative zones can disappear visually after coarse aggregation.
- Absent contracts contribute no exposure, while missing data for listed contracts remains marked unknown. Do not interpolate missing contracts as if open interest existed there or render unknown coverage as a measured zero.
- Label only major axis levels, normally every 100 points, while retaining native strike data internally.

## Smoothing

Smoothing is a rendering operation, not a recalculation:

- Apply a one-dimensional Gaussian filter only along the strike axis for each expiry.
- Keep expiry columns independent. Do not smooth horizontally across dates.
- Default `radius=5` and `sigma=2.25` on a 5-point grid. This removes high-frequency striping while keeping major bands visible.
- Draw the smoothed series with one-pixel linear interpolation. Do not use overlapping translucent pixel rows; overlap creates artificial scan lines.
- Keep net GEX, flips, walls, pits, labels, and text conclusions from raw data. Never substitute the largest all-strike OI shelf for a daily Call/Put Wall; far-OTM legacy OI can dominate without carrying comparable current gamma.
- Keep the spot, flip, call-wall, and put-wall overlays on raw levels; they are not inputs to the color smoothing.
- State in the chart that visual smoothing does not change calculated values.

If the user needs an audit view, disable smoothing to render the native rows; use `--smooth-radius 0` only if the chosen renderer exposes that option.

## Same-Session Comparison

When refreshing a chart during the same session, compare:

- SPX anchor and its distance from the all-window and 0DTE flips;
- 0DTE and all-window net GEX;
- every displayed expiry's net GEX and flip;
- active strikes near spot, including any positive-to-negative or negative-to-positive migration;
- downside pits and upper positive-GEX walls.

Interpret `more negative net GEX` as stronger negative-gamma feedback, not stronger support. A lower flip is not automatically an improvement if spot fell farther and remains below it.

## Validation

- Verify every embedded expiry series has the expected strike count.
- Verify the plotted expiry order exactly matches the JSON's real `expiries` list after de-duplication; do not synthesize missing dates.
- For executable HTML, check JavaScript syntax before delivery.
- Render a desktop preview and inspect axis bounds, current-spot line, flip line, labels, and color continuity.
- Check the header at a 736px-wide preview. Render `CW` and `PW` on separate rows so adjacent expiry columns cannot overlap.
- Confirm the fragment contains no `<html>`, `<head>`, or `<body>` wrapper when the host expects an inline visualization.
- For Codex inline HTML, use a unique root ID and document.getElementById, not document.currentScript; other hosts use their supported rendering path.
- Scan the output for credentials, personal paths, and source JSON paths. None should be embedded.

## Side-specific input contract

The mirrored profile requires `call_gex_by_strike` and `put_gex_by_strike`, supplied by the existing collector. Net-only historical JSON cannot reconstruct the two sides; collect a new snapshot or provide both arrays. The renderer reports the missing field rather than inventing values. An `All` bucket is used only when every supplied expiry is selected. For a subset, both side profiles and Net GEX are summed from the same selected expiries; full-universe aggregate walls and flip are omitted. Missing side data for any selected expiry fails explicitly.
