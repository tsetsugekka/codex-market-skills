# Codex Market Skills

<p align="center">
  <strong>A Codex Skill Suite for trading, investment research, market-move analysis, and market-calendar workflows.</strong>
</p>

<p align="center">
  <a href="README.md">中文</a> |
  <a href="README.en.md">English</a> |
  <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <code>Codex Skill</code> · <code>CN / JP / US Markets</code> · <code>Public-safe</code> · <code>No secrets</code>
</p>

---

> A Codex Skill Suite for trading, investment research, market-move analysis, and market-calendar workflows.

![Codex](https://img.shields.io/badge/Codex-Skill%20Suite-4f46e5)
![Markets](https://img.shields.io/badge/Markets-CN%20%7C%20JP%20%7C%20US-22c55e)
![Language](https://img.shields.io/badge/Language-English-blue)
![Secrets](https://img.shields.io/badge/Secrets-not%20included-critical)

## What This Is

Codex Market Skills is a collection of Codex skills for trading, investment research, and market-calendar workflows. It is organized as a multi-skill repository with separate, clearly scoped market workflows.

It covers four major task areas:

| Area | Coverage |
| --- | --- |
| Stock moves | A-share, Japanese stock, US stock, and ETF moves including rallies, selloffs, volume spikes, limit moves, premarket, and after-hours moves |
| Themes and sentiment | A-share theme strength, short-term sentiment cycles, forum/message-board/community heat, main-line status, and expectation gaps |
| Macro and structure | Macro headlines, broad-market tape, technical structure, support/resistance, gamma/GEX, and 0DTE scenario tables |
| Calendar and reports | US/Japan earnings, macro events, central-bank events, market strategy reports, and closing reviews |

## Skill Overview

| Skill | Purpose | Key Dependencies |
| --- | --- | --- |
| [`market-calendar-google`](docs/market-calendar-google.md) | Organizes earnings, macro data, central-bank events, auctions, and other market events, then writes them to Google Calendar | Required: `google-calendar:google-calendar` |
| [`jp-stock-move-reason`](docs/jp-stock-move-reason.md) | Analyzes Japanese stock moves and produces session-aware regular-market or PTS turnover Top10 lists | None |
| [`cn-stock-move-reason`](docs/cn-stock-move-reason.md) | Analyzes A-share limit-ups, limit-downs, board breaks, volume spikes, and market/sector/stock-level resonance | Optional: `mx-data`, `mx-search`, `mx-xuangu`, `mx-zixuan` |
| [`cn-market-tape`](docs/cn-market-tape.md) | Reads intraday/after-close A-share themes, sector flows, limit-ups, and institutional surveys | Theme ranking: `mx-zixuan`, `mx-xuangu`, `mx-search`; other modules prefer `mx-data` |
| [`stock-sentiment-analysis`](docs/stock-sentiment-analysis.md) | Provides a public-safe sentiment framework reused by other stock skills | Optional: Eastmoney Miaoxiang tools and moomoo community samples |
| [`macro-news-check`](docs/macro-news-check.md) | Checks macro and broad-market context when a stock, index, technical, or gamma analysis needs it | None |
| [`market-daily-strategist`](docs/market-daily-strategist.md) | Produces premarket strategies, closing reviews, and long-term single-name recommendations for US, Japan, and A-share markets | Optional: market data, move-reason, technical, sentiment, and gamma skills |
| [`us-stock-move-reason`](docs/us-stock-move-reason.md) | Uses moomoo news, digest, community, capital, options, and technical anomalies to explain US stock/ETF moves | Optional but recommended: moomoo skills |
| [`us-stock-gamma-moomoo`](docs/us-stock-gamma-moomoo.md) | Uses moomoo OpenD to analyze US options gamma/GEX, gamma walls, and 0DTE scenario tables | Required: local moomoo OpenD and Python SDK `moomoo` |
| [`stock-technical-analysis`](docs/stock-technical-analysis.md) | Analyzes technical structure, support/resistance, volume-price behavior, and indicators for US, Japanese, and A-share stocks | Optional: Eastmoney Miaoxiang tools and `moomoo-technical-anomaly` |

## Highlights

- **One suite for multiple markets**  
  A-shares, Japanese stocks, US stocks, ETFs, indexes, earnings calendars, macro events, and option structure live in one repository while each skill keeps a clear boundary.

- **Public-safe by design**  
  The repository stores only generic workflows, public-safe rules, and scripts. It should not contain watchlists, credentials, API keys, `.env` files, private RAG, runtime caches, or private outputs.

- **Evidence-first market research**  
  Move analysis separates confirmed catalysts, market speculation, forum heat, technical confirmation, macro amplifiers, and background noise.

- **Designed for skill composition**  
  Move-reason, sentiment-cycle, macro-tape, technical-analysis, and gamma-structure skills can be combined when the question needs more than one signal.

- **Chinese reports first**  
  The default operating style is Chinese market research and intraday decision support. English and Japanese READMEs are provided for installation and public documentation.

## Which Skill To Use

| User intent | Recommended skill |
| --- | --- |
| "Why did this A-share hit limit-up, limit-down, or break the board?" | `cn-stock-move-reason` |
| "Is this Japanese stock moving on news or message-board speculation?" | `jp-stock-move-reason` |
| "Run the current Japanese-stock gainers and decliners Top10 by computed turnover, with reasons." | `jp-stock-move-reason` |
| "Why did this US stock move premarket or after hours?" | `us-stock-move-reason` |
| "Which A-share themes are strongest or weakest, and where is money flowing?" | `cn-market-tape` |
| "What does today's limit-up pool or institutional survey heat look like?" | `cn-market-tape` |
| "Is this stock in main-line launch, climax divergence, or retreat rebound?" | `stock-sentiment-analysis` |
| "Is there a macro or broad-market reason behind the move?" | `macro-news-check` |
| "How does the technical setup look right now?" | `stock-technical-analysis` |
| "What does SPX/SPY/single-name option gamma look like?" | `us-stock-gamma-moomoo` |
| "Write a premarket strategy or closing review." | `market-daily-strategist` |
| "Put this week's earnings and market events on the calendar." | `market-calendar-google` |

## Skill Details

<details>
<summary><code>market-calendar-google</code> - Market calendar</summary>

Organizes US earnings, Japan earnings, China/US/Japan macro data, central-bank events, Treasury auctions, and other market-moving events, then writes them to Google Calendar according to the user's rules.

Dependencies: required - `google-calendar:google-calendar`.

Companion skills: none.

Use it to:

- Process this week or next week's Earnings Whispers US earnings image.
- Filter US or Japan earnings through a user watchlist.
- Build a high-importance China/US/Japan market-event calendar.
- Add events in the user's local time while avoiding duplicates.

</details>

<details>
<summary><code>jp-stock-move-reason</code> - Japan stock move reason</summary>

Collects evidence for a user-provided Japanese stock code from Yahoo Finance's live quote page, Yahoo message board, Yahoo/Kabutan/Traders news, and basic stock metrics, then lets Codex analyze the likely reason for the move.

It also includes a mover turnover-ranking sub-skill. On trading days it uses Kabutan's regular mover pages during `09:00-11:30` and `12:30-15:30` JST, PTS day pages during `08:00-09:00`, `11:30-12:30`, and `15:30-17:00`, and PTS night pages at all other times and on non-trading days. It requests 50 rows per page, keeps stocks with an absolute move of at least 3% and volume above 2,000 shares, computes price times volume, and returns gainers and decliners Top10 with reasons.

Dependencies: none.

Companion skills: `stock-sentiment-analysis`, `macro-news-check`, `stock-technical-analysis`.

Use it to:

- Analyze why a Japanese stock is rising, falling, or seeing unusual volume.
- Separate confirmed news catalysts from Yahoo message-board speculation.
- Inspect current change, market cap, PER/PBR, margin ratio, and message-board heat.
- Rank current regular-market or PTS gainers and decliners by computed trading value instead of raw volume.

</details>

<details>
<summary><code>cn-stock-move-reason</code> - A-share move reason</summary>

Collects evidence for one user-provided A-share stock code from Eastmoney public quote data, announcements, and guba/news-like posts, then adds Sohu index/sector context and A-share advance/decline counts so Codex can analyze the likely move reason, market/sector/stock-level resonance, and short-term sentiment-cycle position.

Dependencies: optional - `mx-data`, `mx-search`, `mx-xuangu`, `mx-zixuan` for Eastmoney Miaoxiang enhancement.

Companion skills: `stock-sentiment-analysis`, `macro-news-check`, `stock-technical-analysis`.

Use it to:

- Analyze why an A-share stock hit limit-up, limit-down, broke a board, or saw unusual volume.
- Separate confirmed announcement/earnings catalysts from guba speculation.
- Separate market-wide resonance, sector/concept leadership, and stock-specific catalysts using indexes, sector/concept boards, and advance/decline counts.
- Classify the short-term emotion cycle: ice point, repair/stealth positioning, launch, acceleration, climax, high-level divergence/differentiation, or retreat.

</details>

<details>
<summary><code>cn-market-tape</code> - A-share market tape</summary>

Combines four A-share intraday and after-close modules: weighted theme strength TOP10/BOTTOM10, sector or board main-money flows, the limit-up pool, and institutional survey heat. Theme rankings use local theme mappings plus Eastmoney Miaoxiang quotes; the other modules prefer Miaoxiang aggregate data and fall back to public aggregate sources when a field is unsupported or incomplete. Each result reports its timestamp, data scope, and source change.

Repeated intraday money-flow queries automatically compare the latest same-scope snapshot and keep the result in table form with current value, previous value, change, and rank movement.

Dependencies: theme ranking requires `mx-zixuan`, `mx-xuangu`, and `mx-search`; other modules prefer `mx-data`; institutional surveys use the bundled aggregation script.

Companion skills: `cn-stock-move-reason` and `macro-news-check` only when the user asks for drivers.

Use it to:

- Compute intraday or after-close theme strength TOP10/BOTTOM10.
- Show `Main-money inflow Top10` and `Main-money outflow Top10` in a fixed table format.
- Inspect limit-up counts, consecutive-board ladder, board breaks, and industry/theme distribution.
- Inspect current or historical institutional survey heat, explicitly marking unsupported dates or fields.
- Avoid writing files by default and report host, endpoint family, and error when a fallback source is rate-limited or unstable.

</details>

<details>
<summary><code>stock-sentiment-analysis</code> - Sentiment framework</summary>

Provides a reusable public-safe sentiment and market-emotion framework for A-shares, Japanese stocks, US stocks, indexes, and sector themes. It helps other stock skills classify emotion cycles, main-line versus follower status, expectation gaps, forum/message-board heat, crowded trades, and cross-market risk-on/risk-off context without committing private RAG material.

Dependencies: optional - `mx-data`, `mx-search`, `mx-xuangu` for A-share evidence, theme constituents, and screening; `mx-zixuan` only when the user explicitly asks for watchlist work; `moomoo-comment-sentiment` for US community samples.

Companion skills: `cn-stock-move-reason`, `jp-stock-move-reason`, `us-stock-move-reason`, `stock-technical-analysis`, `us-stock-gamma-moomoo`.

Use it to:

- Synthesize forum/message-board heat, news expectation gaps, breadth, and chart confirmation into a sentiment conclusion.
- Provide a shared sentiment framework for move-reason, technical, and gamma skills.
- When the user provides a private RAG directory, guide them to build a local index with topics, source aliases, page/slide ranges, keywords, and public-safe summaries; never write private source material into this public repository.

</details>

<details>
<summary><code>macro-news-check</code> - Macro headline check</summary>

Checks current macro and broad-market tape for other market skills, but only when a stock, index, technical, or gamma analysis genuinely needs live macro context. The user only needs to ask whether broad-market, macro, cross-asset, or risk-sentiment factors are involved; the skill selects public headline and market-confirmation sources.

Dependencies: none.

Companion skills: none.

Use it to:

- Judge whether a stock or index move is affected by rates, FX, central banks, economic data, commodities, geopolitics, or broad risk-on/risk-off tape.
- Provide macro tape to `cn-stock-move-reason`, `jp-stock-move-reason`, `stock-technical-analysis`, and `us-stock-gamma-moomoo`.
- Turn 2-5 relevant live headlines into a main-driver, secondary-amplifier, or background-noise judgment for the current instrument.

</details>

<details>
<summary><code>market-daily-strategist</code> - Market strategy report</summary>

Routes Chinese market-strategy reports for US, Japan, and A-share markets, covering premarket strategy, closing review, and long-term single-name recommendations. It reads the relevant market/time-window references and compresses macro context, move reasons, sentiment cycle, technical structure, and available local market tools into a decision-oriented report.

Dependencies: optional - `mx-data`, `mx-search`, `mx-xuangu` for A-share market, news, sector/concept constituents; `mx-zixuan` only when the user explicitly asks for watchlist work; official moomoo news, digest, comment, capital, option, and technical anomaly skills for US market enhancement.

Companion skills: `macro-news-check`, `stock-sentiment-analysis`, `stock-technical-analysis`, `cn-stock-move-reason`, `jp-stock-move-reason`, `us-stock-move-reason`, `us-stock-gamma-moomoo`.

Use it to:

- Write US, Japan, or A-share premarket strategy.
- Write US, Japan, or A-share closing review.
- Recommend one US stock, Japanese stock, A-share, ETF, or LOF with entry points, risks, and validation conditions.

</details>

<details>
<summary><code>us-stock-move-reason</code> - US stock move reason</summary>

Combines official moomoo news, stock digest, community sentiment, capital anomalies, option anomalies, technical anomalies, and local gamma/technical/macro skills so Codex can explain why a US stock or ETF moved.

Dependencies: optional but recommended - `moomoo-news-search`, `moomoo-stock-digest`, `moomoo-comment-sentiment`, `moomoo-capital-anomaly`, `moomoo-derivatives-anomaly`, `moomoo-technical-anomaly`; optional - local moomoo OpenD and Python SDK.

Companion skills: `us-stock-gamma-moomoo`, `stock-technical-analysis`, `stock-sentiment-analysis`, `macro-news-check`.

Use it to:

- Analyze why US stocks such as DELL, NVDA, or TSLA rose, fell, gapped premarket, or moved after hours.
- Separate confirmed earnings/guidance/ratings/orders/news from community speculation.
- Check US-applicable option unusual activity, IV, option sentiment, capital flow, short-sale, and technical anomaly evidence.
- Merge macro, technical, and option/gamma structure for SPY/QQQ/SPX-related move questions.

</details>

<details>
<summary><code>us-stock-gamma-moomoo</code> - Option gamma structure</summary>

Uses moomoo OpenD to fetch US stock and option data so Codex can analyze gamma/GEX, gamma walls, gamma flip levels, SPX/SPY/ES intraday structure, and 0DTE option scenario value tables. This skill requires moomoo OpenD to be running locally; if the environment is missing, guide the user to install or launch OpenD first.

Dependencies: required - local moomoo OpenD and Python SDK `moomoo`; optional - `moomoo-derivatives-anomaly` for US option anomalies, unusual trades, IV, PCR, and option sentiment scans.

Companion skills: `macro-news-check`, `stock-technical-analysis`, `stock-sentiment-analysis`, `us-stock-move-reason`.

Use it to:

- Analyze option gamma structure for ordinary US stocks or US-listed ETFs, with optional official moomoo option-anomaly scans for unusual trades, IV, PCR, and option sentiment.
- Analyze `.SPX`/SPXW index-option structure; when direct index data or chains are unavailable, use SPY options, ES/CFD, or a user-provided index anchor for conversion and state the proxy clearly.
- Build time-by-underlying theoretical value tables for 0DTE calls/puts to evaluate recovery, take-profit, or stop levels.
- Output text conclusions, lists, and plain-text tables; for repeated intraday questions in the same conversation, compare with earlier same-session gamma results to judge level migration and strengthening or weakening.

</details>

<details>
<summary><code>stock-technical-analysis</code> - Technical analysis</summary>

Analyzes technical structure for US, Japanese, and A-share stocks, including intraday trend, support/resistance, volume-price behavior, KDJ/MACD/RSI, Vegas channels, chart reads, and whether a stock can reach a target level.

Dependencies: optional - `mx-data`, `mx-search`, `mx-xuangu` for A-share market, news, sector/concept constituents, and technical screening; `mx-zixuan` only when the user explicitly asks for watchlist work; `moomoo-technical-anomaly` for official US technical anomaly scans.

Companion skills: `macro-news-check`, `stock-sentiment-analysis`, `cn-stock-move-reason`, `jp-stock-move-reason`, `us-stock-move-reason`, `us-stock-gamma-moomoo`.

Use it to:

- Classify setups such as trend continuation, high-level consolidation, pullback confirmation, failed breakout, divergence, or breakdown rebound.
- Distinguish touch, break, and tradable hold so one wick is not mistaken for a confirmed breakout.
- Read moomoo/Yahoo/broker charts or screenshots and produce current read, structure, momentum, execution meaning, and next validation level.
- Combine with Japan/A-share move-reason or US gamma skills to judge whether the chart confirms the catalyst.
- For US stocks, use official technical anomalies as prompts, then judge validity through trend position, VWAP/moving averages, volume-price behavior, momentum divergence, support/resistance, and failed breakouts.

</details>

## Installation

In Codex, send the repository URL and ask Codex to install all or selected skills:

```text
Install the Codex skills I need from https://github.com/tsetsugekka/codex-market-skills.
```

If you only need one skill, include its name, such as `stock-technical-analysis` or `cn-market-tape`.

## Example Prompts

```text
Organize next week's Earnings Whispers calendar and add it to Google Calendar.
```

```text
Add this week's four-star-or-higher China/US/Japan market events to Google Calendar.
```

```text
Analyze why 6758 moved today.
```

```text
Check whether 6217 is moving on confirmed news or message-board speculation.
```

```text
Analyze whether 300750 is moving on confirmed announcements or short-term theme emotion.
```

```text
Check current A-share theme strength and show TOP10 and BOTTOM10.
```

```text
Intraday, show which A-share themes are strongest and weakest.
```

```text
Analyze whether this stock is in main-line launch, climax divergence, or retreat rebound.
```

```text
Check whether any broad-market or macro reason is affecting this stock today.
```

```text
Write today's A-share closing review, focusing on main lines, tomorrow's risks, and actionable directions.
```

```text
Check this US stock's gamma and identify resistance plus the most likely levels this week.
```

```text
Price this SPXW 0DTE 7370C across different times and SPX levels.
```

```text
Analyze this stock's technical setup, support, and resistance right now.
```

## Safety Boundaries

- `market-calendar-google` creates or updates Google Calendar events only when the user explicitly asks for calendar changes.
- `jp-stock-move-reason` reads only public webpages/APIs, does not read tokens, does not write to external services, and does not call Gemini/OpenAI APIs.
- `cn-stock-move-reason` reads only public webpages/APIs from Eastmoney, Sohu Securities, and similar public sources; it does not read tokens, write to external services, or call Gemini/OpenAI APIs.
- `cn-market-tape` must use Eastmoney Miaoxiang `mx-zixuan` and `mx-xuangu` for theme strength and only query watchlists; it must not automatically add/delete/modify them. Money flows, limit-ups, and institutional surveys should prefer aggregate Miaoxiang queries; fallback sources must be batched, low-frequency, and randomly delayed. Never commit `MX_APIKEY`, full watchlists, local theme-mapping caches, raw API responses, or runtime caches.
- `stock-sentiment-analysis` stores only public-safe generalized sentiment rules; do not commit private RAG material, personal labels, raw notes, screenshots, or trade logs.
- `macro-news-check` reads only public macro/news pages, feeds, or endpoints; it does not read login cookies, tokens, account data, or private research material, and it should not copy long news text.
- `market-daily-strategist` is a report routing and synthesis layer; local/private market tools are optional enhancements and should not leak watchlists, private outputs, or tool caches into the public repository.
- `us-stock-move-reason` stores only a public-safe US move-reason workflow. Official moomoo skills and OpenD are runtime data layers; do not commit account data, OpenD logs, raw community dumps, private outputs, or personal trade records.
- `us-stock-gamma-moomoo` uses the user's local moomoo OpenD quote interface and does not call trade-unlock APIs. The public version does not depend on private RAG and should not commit account data, OpenD logs, screenshots, private quote outputs, original strategy names, or private person names/handles.
- `stock-technical-analysis` stores only generalized technical-analysis rules. The public version does not depend on private RAG and should not commit personal positions, trade plans, raw screenshots, private research paths, proprietary indicator names, original strategy names, or private person names/handles.
- Do not commit personal watchlists, credentials, API keys, `.env` files, private RAG, runtime caches, or private outputs to this repository.

## Repository Layout

```text
skills/
  market-calendar-google/
    SKILL.md
    agents/openai.yaml
  jp-stock-move-reason/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    scripts/stock_move_sources.py
  cn-stock-move-reason/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    scripts/stock_move_sources.py
  cn-market-tape/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
  stock-sentiment-analysis/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    references/sentiment-framework.md
  macro-news-check/
    SKILL.md
    agents/openai.yaml
  market-daily-strategist/
    SKILL.md
    references/
  us-stock-move-reason/
    SKILL.md
    agents/openai.yaml
  us-stock-gamma-moomoo/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/gamma_report.py
    scripts/option_scenario_table.py
  stock-technical-analysis/
    SKILL.md
    agents/openai.yaml
    references/
docs/
  market-calendar-google.md
  jp-stock-move-reason.md
  cn-stock-move-reason.md
  cn-market-tape.md
  macro-news-check.md
  market-daily-strategist.md
  stock-sentiment-analysis.md
  us-stock-move-reason.md
  us-stock-gamma-moomoo.md
  stock-technical-analysis.md
shared/
  references/release-and-privacy.md
```

## Languages

- 中文：`README.md`
- English: `README.en.md`
- 日本語：`README.ja.md`
