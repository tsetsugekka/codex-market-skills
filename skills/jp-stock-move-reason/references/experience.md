# JP Stock Analysis Experience

Purpose: keep reusable lessons for Japanese stock analysis without forcing the model to read a growing archive every time.

## Active Playbook

Read this section before using the JP stock skill. Keep it compact and current.

### Earnings Reaction Framework

- Predict with `probability x expectation gap x price setup`, not with a single yes/no call.
- For every sharp move, explicitly compare `prior market expectation` versus `actual news`: what investors expected, what actually landed, whether it is above expectation, merely landed/in line, or below expectation. Use both numeric signals such as guidance, profit, orders, dividends, and buybacks, and qualitative signals such as wording strength, timing, certainty, management confidence, regulatory tone, and whether the news solves the market's real concern.
- Set numeric surprise thresholds before the release. Use company guidance, consensus, prior-quarter progress, and peer reactions to define the "strong pass" line before seeing the result.
- For earnings trades, next-period guidance usually matters more than the just-finished period. A clean positive reaction often needs: prior period beat, next year strong guidance, and preferably dividend hike or buyback.
- Low expectations can be powerful. If the market fears "good results still get sold", a merely solid result plus strong guidance/shareholder return can flip the narrative.
- High valuation is not automatically bearish in an accepted megatrend. When a stock sits in a scarce, institutionally accepted theme, strong forward operating/recurring profit guidance can outweigh near-term valuation anxiety.
- Separate `clean beat` from `theme beat with blemishes`. A clean beat clears results, guidance, consensus, and shareholder return. A theme beat may have valuation, net-profit, or consensus blemishes but still work if the future growth story is strengthened.
- Yahoo 掲示板 is useful for reading the expectation gap. If many posts fear "good results still get sold" or "consensus is too high", then a result that clears those exact worries can trigger stronger positive feedback.
- In strong market regimes, the market may reward "strong theme + strong guidance" more than conventional valuation discipline. Adjust the weight of valuation after observing same-day reactions in comparable stocks.

### Cross-Market Theme And Reaction Structure

- Before a catalyst, classify the stock as core theme leader, same-theme follower, defensive/cyclical alternative, old leader rebound, or noise. A good result in a non-core bucket may react less than a merely solid result in the current core theme.
- Theme strength is confirmed by repeated capital return, sector breadth, and peer follow-through, not by one strong stock alone. If only one famous name rises while peers do not follow, treat it as stock-specific or short-term sentiment until proven otherwise.
- After a strong theme run, prepare for both continuation and profit-taking. The question is whether the result extends the next 6-18 month narrative enough to keep money in the theme.
- When the market is strong, broad liquidity can hide weak details; when liquidity cools, guidance quality, order/backlog durability, and valuation discipline matter more.
- Do not pre-commit to the next theme winner. Keep candidates equal until one shows stronger price reaction, guidance surprise, peer confirmation, and 掲示板 expectation reset.
- Old leader rebounds after a new leader weakens can be a warning: it may mean residual positioning and exit liquidity rather than a fresh leadership cycle.

### Practical Checklist Before A Japanese Earnings Release

1. Identify the stock's accepted theme: e.g. EUV/photoresist, AI package substrate, HBM backend, transformer/data-center power, AI semiconductor distribution.
2. Record the current price move, PER/PBR, recent run-up, and 掲示板 heat.
3. From the latest quarter and company forecast, compute the implied remaining-period hurdle.
4. Set a "must beat" line for the release: current-period profit, next-year guidance, orders/backlog, and shareholder returns.
5. State both probabilities: `earnings beat probability` and `positive stock reaction probability`.
6. After the release, classify the result as:
   - `clean positive surprise`
   - `positive but already priced`
   - `mixed but theme strong`
   - `guidance miss`
   - `bad print`

### Reusable Lessons From Recent Cases

- If the current period beats but forward guidance is weak, expect "good result, bad reaction" risk.
- If forward guidance beats consensus/market publications and shareholder return improves, the market can re-rate even after a pre-release run-up.
- If sentiment is skeptical before release and the result clears the feared issue, the reaction can be stronger than the absolute numbers suggest.
- If a stock is a core theme asset, investors may focus on operating profit, recurring profit, order/backlog, capacity contribution, or EBITDA instead of near-term net income.
- If the result is already fully expected, even a good print can produce profit-taking. Look for whether the result changes the next 6-18 month narrative.

### Reasonable Valuation Framework

Use this section when the user asks whether a stock is cheap/expensive, asks for fair value, target range, upside/downside, or valuation after earnings.

- First classify the valuation identity: cyclical resource, semiconductor material, equipment, distributor, power infrastructure, consumer/entertainment, financial, or mixed business. Do not apply one PER range to every company.
- Build at least three anchors: `earnings anchor` such as forward EPS/PER, `quality anchor` such as margin/ROE/FCF/order durability, and `market anchor` such as peer multiples and current theme premium.
- Adjust EPS for capital actions when material: buybacks, tender offers, treasury shares, CB dilution, secondary offerings, splits, parent-company stake reductions, and dividend policy changes.
- Do not count a buyback as purely positive if it is funded by CB or other dilution. Estimate the net effect on share count, EPS, balance sheet, and future dilution risk.
- Separate operating quality from accounting noise. For core-theme stocks, operating profit, recurring profit, orders/backlog, capacity contribution, and EBITDA may matter more than one-year net income; for cyclical stocks, commodity price and FX sensitivity may deserve a lower multiple.
- Use scenario valuation instead of a single point: conservative, base, and bull. State the key assumptions that move the stock from one scenario to another.
- After setting the fair range, compare current price to the range and explain whether the market is pricing current fundamentals, future upgrades, capital policy, or pure sentiment.
- Valuation output should end with a "what must happen to justify upside" test and a "what invalidates the valuation" test.


- For reusable sentiment lessons that apply across markets, update `stock-sentiment-analysis/references/experience.md` as the shared layer, then keep only market-specific details here.

## Compression Protocol

Keep this file readable by compressing before it becomes too large.

- Always read only `Active Playbook` first.
- If a new lesson repeats an existing rule, merge it into the existing bullet instead of appending.
- Keep `Active Playbook` under about 120 lines. When it grows beyond that, rewrite it into fewer higher-signal bullets before adding new material.
- Move detailed older examples into `Archive` only if they still teach a distinct rule. Otherwise delete the detail after preserving the rule.
- Never paste long raw source output here. Store only distilled lessons, dates, tickers, and the rule learned.
- Do not store personal positions, watchlists, unpublished research notes, credentials, cookies, private URLs, or any content that should not be committed to a public repository.

## Conversation Learning Protocol

Use this protocol after multi-turn discussion about the same stock.

- Auto-update experience only when the follow-up reveals a reusable lesson, such as a missed catalyst type, wrong source priority, poor expectation-gap framing, bad valuation weighting, overconfidence, or a recurring output weakness.
- Decide scope before writing: if the lesson applies to both Japanese stocks and A-shares, update both stock-skill `references/experience.md` files; if it relies on Japan-specific sources, rules, or market structure, update only this file.
- Do not update for one-off ticker facts, ordinary user preferences, speculative claims without support, or information that is only useful for the current stock.
- Convert the correction into a general rule before writing it. Prefer one concise bullet in `Active Playbook`; use `Archive` only for distinct dated examples that still teach the rule. The ticker may appear only as a compact example in `Archive`, never as the center of the active rule.
- If the lesson came from a user challenge, capture the analytical failure mode, not the user's private wording. Example: write "When 掲示板 focuses on consensus fear, compare the result against that fear explicitly", not a transcript of the exchange.

## Archive

- 2026-05-11 JP earnings review distilled into the active rules above; ticker-specific details intentionally removed from active guidance to keep the playbook reusable.
- 2026-05-11 Added cross-market emotion-structure rules from an A-share sector discussion transcript; A-share-specific examples and current calls were intentionally omitted.
- 2026-05-15 Added a generalized expectation-gap rule for numeric and qualitative catalysts, so move explanations compare prior expectation with actual news before assigning causality.
