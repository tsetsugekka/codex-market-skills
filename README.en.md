# Codex Market Skills

Codex Market Skills is a collection of Codex skills for trading, investment research, and market-calendar workflows. It is organized as a multi-skill repository with separate, clearly scoped market workflows.

## Included Skills

### [`market-calendar-google`](docs/market-calendar-google.md)

Organizes US earnings, Japan earnings, China/US/Japan macro data, central-bank events, Treasury auctions, and other market-moving events, then writes them to Google Calendar according to the user's rules.

Use it to:

- Process a weekly Earnings Whispers US earnings image.
- Filter US or Japan earnings through a user watchlist.
- Build a high-importance China/US/Japan market-event calendar.
- Add events in the user's local time while avoiding duplicates.

### [`jp-stock-move-reason`](docs/jp-stock-move-reason.md)

Collects evidence for a user-provided Japanese stock code from Yahoo Finance's live quote page, Yahoo message board, Yahoo/Kabutan/Traders news, and basic stock metrics, then lets Codex analyze the likely reason for the move. This skill does not call Gemini or any other LLM API, and it does not read credentials.

Use it to:

- Analyze why a Japanese stock is rising, falling, or seeing unusual volume.
- Separate confirmed news catalysts from Yahoo message-board speculation.
- Inspect current change, market cap, PER/PBR, margin ratio, and message-board heat.

### [`cn-stock-move-reason`](docs/cn-stock-move-reason.md)

Collects evidence for one user-provided A-share stock code from Eastmoney public quote data, announcements, and guba/news-like posts, then adds Sohu index/sector context and A-share advance/decline counts so Codex can analyze the likely move reason, market/sector/stock-level resonance, and short-term sentiment-cycle position. This skill does not call Gemini or any other LLM API, and it does not read credentials.

Use it to:

- Analyze why an A-share stock hit limit-up, limit-down, broke a board, or saw unusual volume.
- Separate confirmed announcement/earnings catalysts from guba speculation.
- Separate market-wide resonance, sector/concept leadership, and stock-specific catalysts using indexes, sector/concept boards, and advance/decline counts.
- Classify the short-term emotion cycle: ice point, repair, launch, acceleration, climax, or retreat.

### [`stock-sentiment-analysis`](docs/stock-sentiment-analysis.md)

Provides a reusable public-safe sentiment and market-emotion framework for A-shares, Japanese stocks, US stocks, indexes, and sector themes. It helps other stock skills classify emotion cycles, main-line versus follower status, expectation gaps, forum/message-board heat, crowded trades, and cross-market risk-on/risk-off context without committing private RAG material.

Use it to:

- Synthesize forum/message-board heat, news expectation gaps, breadth, and chart confirmation into a sentiment conclusion.
- Provide a shared sentiment framework for `cn-stock-move-reason`, `jp-stock-move-reason`, `stock-technical-analysis`, and `us-stock-gamma-moomoo`.
- When the user provides a private RAG directory, guide them to build a local index with topics, source aliases, page/slide ranges, keywords, and public-safe summaries; never write private source material into this public repository.

### [`macro-news-check`](docs/macro-news-check.md)

Checks current macro and broad-market tape for other market skills, but only when a stock, index, technical, or gamma analysis genuinely needs live macro context. It prioritizes Jin10, then uses Wallstreetcn and FinancialJuice for supplementary confirmation.

Use it to:

- Judge whether a stock or index move is affected by rates, FX, central banks, economic data, commodities, geopolitics, or broad risk-on/risk-off tape.
- Provide macro tape to `cn-stock-move-reason`, `jp-stock-move-reason`, `stock-technical-analysis`, and `us-stock-gamma-moomoo`.
- Turn 2-5 relevant live headlines into a main-driver, secondary-amplifier, or background-noise judgment for the current instrument.

### [`us-stock-gamma-moomoo`](docs/us-stock-gamma-moomoo.md)

Uses moomoo OpenD to fetch US stock and option data so Codex can analyze gamma/GEX, gamma walls, gamma flip levels, SPX/SPY/ES intraday structure, and 0DTE option scenario value tables. This skill requires moomoo OpenD to be running locally; if the environment is missing, guide the user to install or launch OpenD first.

Use it to:

- Analyze option gamma structure for ordinary US stocks or US-listed ETFs.
- Analyze `.SPX`/SPXW index-option structure; when direct index data or chains are unavailable, use SPY options, ES/CFD, or a user-provided index anchor for conversion and state the proxy clearly.
- Build time-by-underlying theoretical value tables for 0DTE calls/puts to evaluate recovery, take-profit, or stop levels.
- Output text conclusions, lists, and plain-text tables; for repeated intraday questions in the same conversation, compare with earlier same-session gamma results to judge level migration and strengthening or weakening.

### [`stock-technical-analysis`](docs/stock-technical-analysis.md)

Analyzes technical structure for US, Japanese, and A-share stocks, including intraday trend, support/resistance, volume-price behavior, KDJ/MACD/RSI, Vegas channels, chart reads, and whether a stock can reach a target level. This is a self-contained public-safe skill and does not depend on private RAG.

Use it to:

- Classify setups such as trend continuation, high-level consolidation, pullback confirmation, failed breakout, divergence, or breakdown rebound.
- Distinguish touch, break, and tradable hold so one wick is not mistaken for a confirmed breakout.
- Read moomoo/Yahoo/broker charts or screenshots and produce current read, structure, momentum, execution meaning, and next validation level.
- Combine with move-reason or US gamma skills to judge whether the chart confirms or contradicts a catalyst.

## Installation

In Codex, send the repository URL and ask Codex to install all or selected skills:

```text
Install the Codex skills I need from https://github.com/tsetsugekka/codex-market-skills.
```

If you only need one skill, include its name, such as `stock-technical-analysis` or `cn-theme-strength-mx`.

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
Analyze whether this stock is in main-line launch, climax divergence, or retreat rebound.
```

```text
Check Jin10, Wallstreetcn, and FinancialJuice for any broad-market or macro headlines affecting this stock.
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

## Safety Notes

- `market-calendar-google` creates or updates Google Calendar events only when the user explicitly asks for calendar changes.
- `jp-stock-move-reason` reads only public webpages/APIs, does not read tokens, does not write to external services, and does not call Gemini/OpenAI APIs.
- `cn-stock-move-reason` reads only public webpages/APIs from Eastmoney, Sohu Securities, and similar public sources; it does not read tokens, write to external services, or call Gemini/OpenAI APIs.
- `stock-sentiment-analysis` stores only public-safe generalized sentiment rules; do not commit private RAG material, personal labels, raw notes, screenshots, or trade logs.
- `macro-news-check` reads only public macro/news pages, feeds, or endpoints; it does not read login cookies, tokens, account data, or private research material, and it should not copy long news text.
- `us-stock-gamma-moomoo` uses the user's local moomoo OpenD quote interface and does not call trade-unlock APIs. The public version does not depend on private RAG and should not commit personal account data, OpenD logs, screenshots, private quote outputs, original strategy names, or private person names/handles.
- `stock-technical-analysis` stores only generalized technical-analysis rules. The public version does not depend on private RAG and should not commit personal positions, trade plans, raw screenshots, private research paths, proprietary indicator names, original strategy names, or private person names/handles.
- If personal study materials are useful, keep them in a private RAG/knowledge base outside this public repository and copy back only distilled generic rules.
- Do not commit personal watchlists, credentials, `.env` files, runtime caches, or private outputs to this repository.

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
  stock-sentiment-analysis/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    references/sentiment-framework.md
  macro-news-check/
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
  cn-theme-strength-mx.md
  macro-news-check.md
  market-daily-strategist.md
  stock-sentiment-analysis.md
  us-stock-gamma-moomoo.md
  stock-technical-analysis.md
shared/
  references/release-and-privacy.md
```

## Languages

- 中文：`README.md`
- 日本語：`README.ja.md`
- English: `README.en.md`
