# Codex Market Skills

Codex Market Skills is a collection of Codex skills for trading, investment research, and market-calendar workflows. The project originally contained only `market-calendar-google`; it is now organized as a multi-skill repository with separate, clearly scoped market workflows.

## Included Skills

### [`market-calendar-google`](skills/market-calendar-google/README.md)

Organizes US earnings, Japan earnings, China/US/Japan macro data, central-bank events, Treasury auctions, and other market-moving events, then writes them to Google Calendar according to the user's rules.

Use it to:

- Process a weekly Earnings Whispers US earnings image.
- Filter US or Japan earnings through a user watchlist.
- Build a high-importance China/US/Japan market-event calendar.
- Add events in Japan time while avoiding duplicates.

### [`jp-stock-move-reason`](skills/jp-stock-move-reason/README.md)

Collects evidence for a user-provided Japanese stock code from Yahoo Finance's live quote page, Yahoo message board, Yahoo/Kabutan/Traders news, and basic stock metrics, then lets Codex analyze the likely reason for the move. This skill does not call Gemini or any other LLM API, and it does not read credentials.

Use it to:

- Analyze why a Japanese stock is rising, falling, or seeing unusual volume.
- Separate confirmed news catalysts from Yahoo message-board speculation.
- Inspect current change, market cap, PER/PBR, margin ratio, and message-board heat.

### [`cn-stock-move-reason`](skills/cn-stock-move-reason/README.md)

Collects evidence for one user-provided A-share stock code from Eastmoney public quote data, announcements, and guba/news-like posts, then adds Sohu index/sector context and A-share advance/decline counts so Codex can analyze the likely move reason, market/sector/stock-level resonance, and short-term sentiment-cycle position. This skill does not call Gemini or any other LLM API, and it does not read credentials.

Use it to:

- Analyze why an A-share stock hit limit-up, limit-down, broke a board, or saw unusual volume.
- Separate confirmed announcement/earnings catalysts from guba speculation.
- Separate market-wide resonance, sector/concept leadership, and stock-specific catalysts using indexes, sector/concept boards, and advance/decline counts.
- Classify the short-term emotion cycle: ice point, repair, launch, acceleration, climax, or retreat.

### [`us-stock-gamma-moomoo`](skills/us-stock-gamma-moomoo/SKILL.md)

Uses moomoo OpenD to fetch US stock and option data so Codex can analyze gamma/GEX, gamma walls, gamma flip levels, SPX/SPY/ES intraday structure, and 0DTE option scenario value tables. This skill requires moomoo OpenD to be running locally; if the environment is missing, guide the user to install or launch OpenD first.

Use it to:

- Analyze gamma structure for BA, MP, TEL, MRVL, SLV, SPY, QQQ, `.SPX`/SPXW, and similar names.
- Convert SPY/ES/CFD context into SPX-equivalent levels for intraday support, resistance, repair, and invalidation zones.
- Build time-by-underlying theoretical value tables for 0DTE calls/puts to evaluate recovery, take-profit, or stop levels.
- Generate a local HTML gamma report when useful, or answer quickly in chat for fast intraday questions.

## Installation

Clone the repository anywhere, then copy or symlink the skills you want into `~/.codex/skills/`.

```bash
git clone https://github.com/tsetsugekka/codex-market-skills.git
mkdir -p ~/.codex/skills
ln -s /path/to/codex-market-skills/skills/market-calendar-google ~/.codex/skills/market-calendar-google
ln -s /path/to/codex-market-skills/skills/jp-stock-move-reason ~/.codex/skills/jp-stock-move-reason
ln -s /path/to/codex-market-skills/skills/cn-stock-move-reason ~/.codex/skills/cn-stock-move-reason
ln -s /path/to/codex-market-skills/skills/us-stock-gamma-moomoo ~/.codex/skills/us-stock-gamma-moomoo
```

You can install only one skill if that is all you need.

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
Check BA gamma and identify resistance plus the most likely levels this week.
```

```text
Price this SPXW 0DTE 7370C across different times and SPX levels.
```

## Safety Notes

- `market-calendar-google` creates or updates Google Calendar events only when the user explicitly asks for calendar changes.
- `jp-stock-move-reason` reads only public webpages/APIs, does not read tokens, does not write to external services, and does not call Gemini/OpenAI APIs.
- `cn-stock-move-reason` reads only public webpages/APIs from Eastmoney, Sohu Securities, and similar public sources; it does not read tokens, write to external services, or call Gemini/OpenAI APIs.
- `us-stock-gamma-moomoo` uses the user's local moomoo OpenD quote interface, does not call trade-unlock APIs, and should not commit personal account data, OpenD logs, screenshots, or private quote outputs.
- Do not commit personal watchlists, credentials, `.env` files, runtime caches, or private outputs to this repository.

## Repository Layout

```text
skills/
  market-calendar-google/
    SKILL.md
    README.md
    agents/openai.yaml
  jp-stock-move-reason/
    SKILL.md
    EXPERIENCE.md
    README.md
    scripts/stock_move_sources.py
  cn-stock-move-reason/
    SKILL.md
    EXPERIENCE.md
    README.md
    agents/openai.yaml
    scripts/stock_move_sources.py
  us-stock-gamma-moomoo/
    SKILL.md
    references/
    scripts/gamma_report.py
    scripts/option_scenario_table.py
```

## Languages

- 中文：`README.md`
- 日本語：`README.ja.md`
- English: `README.en.md`
