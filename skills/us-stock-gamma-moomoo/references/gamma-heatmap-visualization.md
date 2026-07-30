# SPX Gamma Heatmap Visualization

Use this reference when the user asks for a chart similar to a multi-expiry gamma surface, wants the current chart refreshed, or asks for smoother heatmap rendering.

## Chart Semantics

- Horizontal axis: real listed SPX/SPXW expiries returned by OpenD. Never invent a missing daily expiry.
- Vertical axis: SPX strike levels, normally using the native 5-point spacing near spot.
- Heatmap color: signed GEX by strike for each expiry at the current SPX pricing anchor.
- Left bars: all-selected-expiry GEX aggregated at each strike.
- Solid line: each expiry's self-calculated gamma flip. This is a regime boundary, not a predicted SPX path.
- Dashed line: current SPX pricing anchor.
- Dotted point line: each expiry's self-calculated rough magnet. This is a positive-GEX pinning-center estimate, not support, a target, or a predicted price path.
- Call-wall line: the `call_wall.level` calculated only from that expiry's contracts, meaning the strike with the largest call-side GEX at the current anchor.
- Put-wall line: the `put_wall.level` calculated only from that expiry's contracts, meaning the strike with the most negative put-side GEX at the current anchor. It is not automatic support after price loses it.
- Positive and negative colors must use host theme variables. Do not hard-code light/dark colors.

This chart is a transparent, self-calculated OpenD view. Do not claim that it reproduces a proprietary vendor's forward gamma model.

## Data Workflow

1. Run `spx_intraday_latest.py` with `--by-expiry-report`, a sufficient `--future-count`, and a temporary `--json-output`.
2. Confirm that the JSON contains `spot_anchor`, `expiries`, `per_expiry`, and `buckets.All`.
3. Use `render_spx_gamma_heatmap.py` to generate an HTML fragment.
4. Render or preview the fragment, then show it through the host's inline visualization path. Do not build or publish a website unless the user explicitly requests one.
5. Keep the JSON only when comparison or audit work still needs it; otherwise treat it as temporary.

Example:

```bash
python3 scripts/spx_intraday_latest.py \
  --by-expiry-report --future-count 6 \
  --json-output /tmp/current-spx-gamma.json

python3 scripts/render_spx_gamma_heatmap.py \
  /tmp/current-spx-gamma.json /tmp/spx-gamma.html \
  --min-strike 7000 --max-strike 7700 \
  --smooth-radius 5 --smooth-sigma 2.25
```

The output is an inline HTML fragment, not a standalone page. It contains only the normalized chart payload: expiry dates, spot, raw 5-point GEX arrays, flips, rough magnets, summary values, and the selected rendering parameters. It does not embed the source/output path or identity-derived metadata.

For Codex inline display, keep the fragment in the thread-scoped visualization directory and emit `::codex-inline-vis{file="basename.html"}`. The directive must use only the file name, not an absolute path. The fragment root must have a generated unique ID and the script must select it with `document.getElementById`; do not use `document.currentScript`.

## Rough Magnet Compatibility

- Prefer each `per_expiry[date].rough_magnet.level` produced by the gamma calculator.
- Older JSON may not contain `rough_magnet`. The renderer then uses positive GEX strikes within 250 points of spot and weights each strike by `positive_gex * exp(-distance_from_spot / 100)`.
- Round the resulting weighted centroid to the native 5-point strike grid.
- If no positive GEX exists in the window, leave the magnet missing. Do not substitute a wall, pit, flip, or zero, and do not connect the point line across that missing expiry.
- The fallback exists for file compatibility. It must stay mathematically aligned with the calculator's rough-magnet method.
- Never smooth or interpolate magnet levels across expiries. Every plotted point belongs to one real listed expiry.

## Range And Granularity

- Honor a user-specified range exactly when the option-chain data covers it.
- If no range is supplied, choose a range around spot that exposes both the nearest repair zone and downside risk area.
- Do not replace native 5-point strikes with 25-point buckets merely to reduce row count. Broad negative zones can disappear visually after coarse aggregation.
- Missing exact strikes remain zero in the GEX-by-strike map. Do not interpolate missing contracts as if open interest existed there.
- Label only major axis levels, normally every 100 points, while retaining native strike data internally.

## Smoothing

Smoothing is a rendering operation, not a recalculation:

- Apply a one-dimensional Gaussian filter only along the strike axis for each expiry.
- Keep expiry columns independent. Do not smooth horizontally across dates.
- Default `radius=5` and `sigma=2.25` on a 5-point grid. This removes high-frequency striping while keeping major bands visible.
- Draw the smoothed series with one-pixel linear interpolation. Do not use overlapping translucent pixel rows; overlap creates artificial scan lines.
- Keep net GEX, flips, walls, pits, labels, and text conclusions from raw data. Never substitute the largest all-strike OI shelf for a daily Call/Put Wall; far-OTM legacy OI can dominate without carrying comparable current gamma.
- Keep the spot, flip, magnet, call-wall, and put-wall overlays on raw levels; they are not inputs to the color smoothing.
- State in the chart that visual smoothing does not change calculated values.

If the user needs an audit view, set `--smooth-radius 0` to render the native unsmoothed rows.

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
- Test both a current JSON with `rough_magnet` and an older JSON that exercises the renderer fallback.
- Compile the generated JavaScript before delivery.
- Render a desktop preview and inspect axis bounds, current-spot line, flip line, labels, and color continuity.
- Check the header at a 736px-wide preview. Render `CW` and `PW` on separate rows so adjacent expiry columns cannot overlap.
- Confirm the fragment contains no `<html>`, `<head>`, or `<body>` wrapper when the host expects an inline visualization.
- Confirm the root has a unique ID, `document.currentScript` is absent, and the final inline directive uses only the fragment file name.
- Scan the output for credentials, personal paths, and source JSON paths. None should be embedded.
