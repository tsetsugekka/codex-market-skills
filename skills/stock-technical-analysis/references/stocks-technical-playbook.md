# Stocks Technical Playbook

Compressed reusable technical-analysis lessons. This reference is self-contained; private source paths, proprietary indicator names, and personal strategy labels are intentionally omitted.

## 1. First Classify The Setup

Before indicators, name the structure:

- `强趋势延续`: price above key moving averages, pullbacks shallow, volume confirms advances.
- `空中加油候选`: strong advance followed by high-level sideways/narrow consolidation; not valid until it avoids breakdown and breaks upward with volume.
- `回踩确认`: price pulls back to support, volume contracts on the pullback, rebounds with volume, and momentum does not deteriorate materially.
- `冲高回落`: intraday high fails, price returns below pressure, volume is heavy but price no longer advances.
- `高位分歧`: attention and volatility are high, leaders hesitate, followers weaken, or momentum diverges.
- `破位反抽`: support is lost, rebound cannot reclaim the broken level with volume.

Do not call a move bullish just because it is green. A high green candle after an early spike may still be distribution if it cannot reclaim pressure with volume.

## 2. Volume-Price Rules

Volume is the cause, price is the result.

- `放量上涨`: constructive when it breaks and stands above pressure.
- `缩量上涨`: momentum may be insufficient, especially near pressure.
- `放量不涨`: possible distribution or failed breakout.
- `放量下跌`: real selling pressure, unless it is a panic low followed by immediate reclaim.
- `缩量回踩`: can be healthy if support holds and the next rebound brings volume.

Breakout rule:

- A level is not truly broken by one wick.
- Prefer a close above the level, especially on a 5-minute bar for intraday or daily close for swing.
- Breakout should come with increased volume and better order-flow quality.
- If price breaks above resistance then falls back quickly, treat it as an unconfirmed breakout.

High-open rule:

- A large high open needs follow-through.
- If the open is more than 5% above the prior close and does not attract real buying, beware high-open fade.
- If the stock rises alone while the sector or peers do not confirm, sustainability is weaker.

Intraday timing cues:

- Around 09:45, a very high volume ratio can mean real participation or early distribution; judge by whether price keeps advancing.
- Around 13:15, the first afternoon lift should have volume; no volume often leads to pullback.
- Around 14:50, a sudden late ramp can be fragile next day if unsupported by broader structure.

## 3. Moving Averages And Vegas Framework

Use multiple timeframes. Do not let a 1-minute chart overrule a damaged 5-minute or daily structure.

Core moving average ideas:

- 5-day line: short-term momentum. A quick reclaim after a break can be a washout; failure to reclaim is risk.
- 20-day line: institutional life line. Effective break plus failed reclaim implies trend damage.
- Slope matters: the steeper the line after a large rise, the higher the reaction risk.
- Support can become resistance after it is broken.

Vegas-style channel framework:

- `EMA144 / EMA169`: medium-term trend tunnel.
- `EMA576 / EMA676`: long-term trend tunnel and major support/resistance.
- `MA144 low`: low-price support reference.
- `EMA5 / EMA21`: short-term momentum and pullback guide.

Read:

- Price above rising EMA144/169 and EMA576/676: trend is structurally strong.
- EMA144 crossing above EMA169: medium-term bullish confirmation.
- EMA144 crossing below EMA169: medium-term bearish warning.
- Pullback to EMA144/169 that holds can be a setup; failure to reclaim it weakens the trend.

EMA tunnel rebound-continuation setup:

- Starts after a fast decline, rebound, and base-building phase around a medium-term EMA tunnel.
- The useful signal is not the first bounce, but a later close back above the EMA144/169 area after the short-term averages compress.
- Prefer to see two momentum confirmations: one near the initial low/rebound attempt and another near the later pullback or base tail. KDJ low-level crosses are useful here, especially if the second low is higher or selling volume contracts.
- Treat the setup as continuation only after price reclaims the medium-term tunnel and holds; otherwise it is just a rebound inside a damaged trend.
- Upside measurement can use the base width or prior pressure zones, but only after the breakout is confirmed.

## 4. KDJ

Base formula:

- RSV uses close position inside recent high-low range.
- K and D smooth RSV.
- J = 3K - 2D.

Use:

- Low-level K crossing above D: possible rebound signal, stronger with support and volume.
- High-level K crossing below D: short-term risk, especially after a big rise.
- J below 10: extreme weakness/panic zone; look for reversal only after confirmation.
- K above 90 and J above 100: overheated risk.
- Price makes lower low while K makes higher low and K crosses D: bottom divergence candidate.
- Price makes higher high while K makes lower high and D crosses above K: top divergence candidate.

KDJ alone is not enough. In a strong trend it can stay high; in a weak trend it can keep failing.

## 5. MACD

Use MACD as trend and momentum confirmation.

- DIF/DEA above zero and DIF crosses above DEA: stronger bullish signal.
- DIF/DEA below zero and DIF crosses below DEA: stronger bearish signal.
- Red bars turning smaller: upside momentum weakening.
- Green bars turning smaller or flipping red: downside pressure easing.
- Price makes a new high while MACD does not: top divergence risk.
- Zero-axis context matters: a golden cross above zero is stronger than one below zero; a dead cross above zero can be only a pullback if key support holds.

MACD-RSI-KDJ composite momentum check:

- Bottom-risk/rebound area: MACD below zero, KDJ/J deeply depressed, and RSI low. This is not a buy signal by itself; require support defense, selling exhaustion, or a reclaim of a short-term average.
- Strong rebound confirmation: MACD green bars shrink or flip, KDJ crosses up from low/mid levels, and RSI turns up from weak levels.
- Top-risk area: MACD above zero, J above 80, RSI above 60-70, and K crossing below D after a sharp rise.
- Trend exception: in a powerful trend, high RSI/KDJ can persist. Reduce exposure to oscillator-only conclusions unless price also fails at pressure, loses support, or prints momentum divergence.

## 6. RSI

RSI is a context indicator, not an automatic sell/buy switch.

- RSI above 70 means overbought risk, but strong trends can stay overbought.
- RSI below 30 means oversold, but weak stocks can stay weak.
- Price new high with RSI not confirming is a warning.
- Use RSI with moving averages, K-line structure, and volume.

VWAP-based RSI:

- Some chart setups use RSI calculated on VWAP rather than on raw close. Treat it as a measure of momentum relative to the market's volume-weighted trading center.
- A practical default is length around 16, with roughly 18 as deeply oversold and 80 as overbought. These thresholds are references, not mechanical orders.
- A cross back above the oversold line can mark selling exhaustion or a rebound attempt, especially if price defends support or reclaims VWAP/short averages.
- A cross back below the overbought line can mark partial profit-taking or cooling after an extended move, especially if price also fails at resistance.
- In a strong catalyst trend, VWAP-based RSI may stay high while price rides above VWAP. Do not treat overbought alone as bearish unless support conversion fails, volume-price stalls, or momentum diverges.
- In a weak or falling trend, oversold rebounds are lower quality unless price reclaims VWAP and creates a higher low.

## 7. Support And Resistance

Support/resistance sources:

- Prior high and prior low.
- Intraday high/low after a large event.
- VWAP and obvious volume-weighted areas.
- 5/20-day moving averages.
- Vegas EMA144/169 and EMA576/676.
- Dense chip/volume areas.
- Bollinger upper/lower bands if visible.

Pressure rule:

- Do not chase directly into major pressure.
- A breakout needs volume and standing above the level.
- A failed reclaim of prior support is resistance.

Support rule:

- A support is valid only if price reacts there and can reclaim short-term averages.
- If support breaks with volume and cannot recover quickly, treat the trend as damaged.

## 8. 空中加油

Definition:

- A strong stock rises sharply, then consolidates at a high level instead of collapsing.
- The consolidation is relatively narrow, volume does not show obvious distribution, and key support holds.
- A renewed breakout must come with volume.

Valid clues:

- Price does not fall below the consolidation lower bound.
- Pullback volume shrinks.
- Rebound volume expands.
- Moving averages remain in bullish order.
- MACD/RSI do not clearly deteriorate.

Invalid clues:

- Long upper shadows keep appearing near the same pressure.
- Volume rises but price cannot advance.
- KDJ/MACD weaken while price holds only because of retail enthusiasm.
- Key support breaks and cannot be reclaimed.

## 9. 回踩, 破位, And 破五反五

Healthy pullback:

- Pullback to support without heavy selling.
- Rebound has volume.
- 5-minute/daily moving average structure remains intact.
- MACD/RSI are stable or improve.

Breakdown:

- Key support breaks and cannot quickly recover.
- Selling volume expands.
- MACD green bars expand or dead cross confirms.
- Rebound fails at the broken support.

破五反五:

- A short break below the 5-day line is not fatal if price quickly reclaims the 5-day line.
- Reclaim should ideally be supported by volume.
- If price breaks but cannot stand back above the 5-day line, beware further selling.

## 10. Candlestick Context

Read candles in context, not as isolated names.

- Long upper shadow after a large rise near resistance: supply appears.
- Long lower shadow at support with volume: possible defense.
- Big candle with high turnover after a long rise: can be climax or distribution.
- Narrow high-level consolidation can be bullish only if support and volume behavior are healthy.
- Repeated failed highs at the same level are pressure confirmation.

## 11. A-Share Emotion Overlay

For A-shares, combine technicals with the emotion cycle:

- `冰点`: observe who resists.
- `修复/潜伏`: small trial setups, look for early leaders.
- `启动`: prefer front-row names.
- `加速`: hold strength, avoid late random laggards.
- `高潮`: do not chase heavily; take profit thinking matters.
- `高位分歧/分化`: distinguish healthy turnover from emotional top.
- `退潮`: reduce risk; failed rebounds are common.

Technical signals near emotion climax need stricter confirmation. A breakout during early cycle can work with less perfection; a breakout after broad climax needs stronger volume and leadership confirmation.

## 12. Intraday "Can It Reach X?" Framework

When the user asks whether a stock can reach a target price today:

1. Mark current price, target, day high, day low, open, previous close, and nearest pressure.
2. Decide whether the target is below prior high, at prior high, or a new high.
3. If target is near or above prior high, require a reclaim of the nearest pressure first.
4. Check 1-minute and 5-minute charts:
   - 1-minute: timing and immediate momentum.
   - 5-minute: whether the move has structure.
5. Check volume:
   - Rising volume on attack is constructive.
   - Shrinking volume on attack is fragile.
   - Heavy volume but no progress is warning.
6. Check KDJ/MACD:
   - KDJ golden cross plus MACD improvement supports attack.
   - KDJ dead cross plus weakening MACD argues for pullback first.
7. Give a conditional probability:
   - Before pressure is reclaimed: lower or neutral probability.
   - After pressure is reclaimed and held with volume: probability improves.
   - After key support breaks: probability falls sharply.

Execution realism:

- Distinguish `touching X` from `standing above X`. A fast wick through the target may not give the user a practical exit or entry.
- For an exit target, treat the surrounding pressure band as the decision area. If price repeatedly touches the band and is immediately rejected, say that waiting for a clean hold above the exact level may reduce execution quality.
- For a continuation target, require the level to become support: hold above it, retest without heavy selling, or print a higher low above the reclaimed level.
- When a stock moves from rejected resistance back above the prior support and attacks again, do not over-penalize the first rejection. The support hold plus renewed attack can be the useful signal.

Use exact levels from live data where possible. If the chart data is stale or visually uncertain, say so.

## 13. Chart App Visual Workflow

Use this when reading moomoo, Yahoo Finance charts, broker apps, or screenshots.

Before acting:

- Confirm the ticker/name on screen. If the app is showing a different stock than the user asked about, switch or say so before analysis.
- Confirm chart timeframes and whether the visible chart is live, delayed, or screenshot-based.
- Prefer reading at least two timeframes:
  - `1m/3m`: timing, immediate pressure, quick execution.
  - `5m/15m`: intraday structure and whether a move is tradable.
  - `1h`: whether intraday strength is aligned with a larger trend or already overextended.
  - `Daily`: gap, prior highs/lows, longer pressure/support, and whether the move is a breakout or exhaustion.

Chart elements to read:

- Price: current price, day high/low, open, previous close, recent swing highs/lows, and the nearest exact pressure/support.
- Volume: whether attack bars expand, pullback bars contract, and whether heavy volume fails to move price.
- Moving averages/price bands: whether price is above/below the short average cluster, whether a reclaimed level becomes support, and whether price is stretched outside bands.
- Momentum: KDJ, MACD, RSI, and VWAP-based RSI if visible. Treat high oscillators as heat warnings; do not override orderly higher lows in a strong trend.
- Funding/order-flow panels: use large/small order flow, capital-flow charts, bid/ask quality, and sector/peer list as context, not as standalone proof.
- Peer/sector watchlist: confirm whether same-theme leaders/followers are moving together or whether the stock is isolated.

Visual-analysis discipline:

- Do not infer precise numeric values from a chart if the labels are unreadable. Say the value is approximate or ask for a clearer view.
- Treat one visible candle as provisional. For intraday confirmation, prefer a 5-minute close, a clean retest, or repeated support above the reclaimed level.
- If the user changes timeframe, re-evaluate instead of carrying over the prior 1-minute conclusion.
- When the app shows a popover/list instead of the chart, return to the main chart before analyzing.
- If multiple charts are visible, specify which one drives the conclusion and which one is only supporting evidence.

Output from chart-app analysis should include:

- `当前读数`: price, timeframe, and whether the source is live/visual.
- `结构`: trend, pressure/support, and whether the setup is confirmed or only a candidate.
- `量价/动能`: volume and key indicator read.
- `执行含义`: distinguish touch/break/tradable hold; separate intraday profit-taking from trend holding if both matter.
- `下一验证点`: the exact level or candle behavior that would change the conclusion.

## 14. Response Guardrails

- Do not issue direct buy/sell commands.
- State the data source and whether it is live, delayed, screenshot-based, or inferred.
- Separate `already confirmed` from `candidate setup`.
- Name the bullish trigger and bearish invalidation.
- When uncertain, say what information would decide it: volume, 5-minute close, VWAP, peer confirmation, or order-flow quality.
