# Codex Market Skills

Codex Market Skills is a collection of Codex skills for trading, investment research, and market-calendar workflows. The project originally contained only `market-calendar-google`; it is now organized as a multi-skill repository with separate, clearly scoped market workflows.

## Included Skills

### `market-calendar-google`

Organizes US earnings, Japan earnings, China/US/Japan macro data, central-bank events, Treasury auctions, and other market-moving events, then writes them to Google Calendar according to the user's rules.

Use it to:

- Process a weekly Earnings Whispers US earnings image.
- Filter US or Japan earnings through a user watchlist.
- Build a high-importance China/US/Japan market-event calendar.
- Add events in Japan time while avoiding duplicates.

### `jp-stock-move-reason`

Collects evidence for a user-provided Japanese stock code from Yahoo Finance's live quote page, Yahoo message board, Yahoo/Kabutan/Traders news, and basic stock metrics, then lets Codex analyze the likely reason for the move. This skill does not call Gemini or any other LLM API, and it does not read credentials.

Use it to:

- Analyze why a Japanese stock is rising, falling, or seeing unusual volume.
- Separate confirmed news catalysts from Yahoo message-board speculation.
- Inspect current change, market cap, PER/PBR, margin ratio, and message-board heat.

## Installation

Clone the repository anywhere, then copy or symlink the skills you want into `~/.codex/skills/`.

```bash
git clone https://github.com/tsetsugekka/codex-market-skills.git
mkdir -p ~/.codex/skills
ln -s /path/to/codex-market-skills/skills/market-calendar-google ~/.codex/skills/market-calendar-google
ln -s /path/to/codex-market-skills/skills/jp-stock-move-reason ~/.codex/skills/jp-stock-move-reason
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

## Safety Notes

- `market-calendar-google` creates or updates Google Calendar events only when the user explicitly asks for calendar changes.
- `jp-stock-move-reason` reads only public webpages/APIs, does not read tokens, does not write to external services, and does not call Gemini/OpenAI APIs.
- Do not commit personal watchlists, credentials, `.env` files, runtime caches, or private outputs to this repository.

## Repository Layout

```text
skills/
  market-calendar-google/
    SKILL.md
    agents/openai.yaml
  jp-stock-move-reason/
    SKILL.md
    scripts/stock_move_sources.py
```

## Languages

- 中文：`README.md`
- 日本語：`README.ja.md`
- English: `README.en.md`
