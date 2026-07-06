---
name: market-calendar-google
description: Organize a selected week of US earnings calendars or China/US/Japan macro and market-event calendars, prioritize what matters to the user, and add the resulting events to Google Calendar. Use when the user asks to handle this week's or next week's earnings, Earnings Whispers images, US stock ticker earnings, Treasury auctions, central-bank/data releases, or China/US/Japan financial events and wants them written to Google Calendar.
---

# Market Calendar Google

## Overview

Use this skill to turn weekly market calendars into concise Google Calendar events for the user. Support three workflows:

1. US earnings calendar for a week, usually from the Earnings Whispers "Most Anticipated Earnings Releases" image.
2. China/US/Japan macro, central-bank, auction, and market-event calendar for a week.
3. Japan stock earnings calendar for a week, usually from SBI Securities settlement announcement data.

Default to the user's local timezone from the runtime environment. Use the current date and timezone from the environment to resolve "this week" and "next week". If the user's timezone is unavailable, ask for the target timezone before writing Calendar events.

## Shared Rules

- This skill depends on the `google-calendar:google-calendar` skill/connector whenever the user wants events written to Google Calendar.
- When Calendar writing is requested, first ensure Google Calendar tools are available. If they are not already loaded, use `tool_search` with a query such as `Google Calendar search create event` to surface the Google Calendar tools before doing calendar work.
- If Google Calendar tools still are not available, tell the user the exact next action: connect or install the Google Calendar connector/skill, then stop before claiming events were written.
- If a Calendar write fails with an authorization/authentication error such as `401`, `UNAUTHORIZED`, `PERMISSION_DENIED`, expired token, missing scope, or write access failure, do not just repeat the raw error. Handle it as an actionable connector state:
  - First, try the least disruptive recovery path available in the current environment, such as loading the `google-calendar:google-calendar` skill/tools with `tool_search`, re-reading a bounded calendar window, and retrying the same write once if the connector becomes available.
  - If the environment exposes a connector install/authorization flow, ask the user to approve that concrete flow or invoke the relevant install/authorization request instead of asking them to diagnose OAuth/scopes.
  - If automatic recovery is not possible, tell the user exactly what to do in one sentence, for example: "请在 Codex 的 Google Calendar 连接里重新授权写入权限，然后我会继续创建这些日程。"
  - Preserve the prepared event payloads and duplicate-check results in the response so the user can retry without reconstructing the calendar work.
  - Never claim events were written unless a follow-up bounded search verifies the created or updated events.
- Use Google Calendar tools. Search the target week first to avoid duplicates before creating or updating events.
- Preserve existing user-created calendar details unless the user asks to overwrite them.
- Put a country flag at the start of titles when the event has a clear country:
  - US: `🇺🇸`
  - China: `🇨🇳`
  - Japan: `🇯🇵`
- If several events fall in the same 30-minute bucket, combine them into one event. Buckets are `:00-:29` and `:30-:59`.
- If combined events are all from the same country, use the flag only once. If countries differ, include each relevant flag before its event name.
- Do not combine earnings events (`ER` or `決算`) with macro, auction, holiday, political, central-bank, conference, index-change, or other market-event items. Even if they fall in the same 30-minute bucket, create separate Calendar events. The 30-minute combining rule applies only within the same workflow/category.
- Use the user's local-time event times in Calendar. Convert source-market event times into the user's local timezone before writing events. In descriptions, write in Chinese unless the user asks otherwise.
- For 5-star events, set Google Calendar event color to red (`color_id: "11"` after confirming colors if needed).
- Prefer transparent events for informational market calendar items unless the existing event uses a different setting or the user asks to block the calendar.
- Do not include process/source boilerplate such as "parsed from image", local file paths, or explanations of why something was included. Include actionable market notes instead.
- Do not repeat information that is already obvious from the calendar title or time slot. For example, avoid writing "title focus", redundant timezone labels, session labels, or the same event list twice unless that detail adds new useful context.
- In Google Calendar descriptions, use `・` for bullet-like lines instead of leading hyphen bullets. The connector may persist leading `-` as escaped `\-`.
- For US earnings, the default personal watchlist source is the user's moomoo watchlist via the `us-stock-gamma-moomoo` skill/OpenD workflow. If it is unavailable or incomplete, `https://daytrading.monster/themes/theme-data.json` may be used as the backup candidate theme list.
- For Japan earnings, the default candidate list source is `https://daytrading.monster/themes/theme-data.json`, because local moomoo OpenD may not expose individual Japan stock watchlist codes. If the user provides a Japan CSV or another usable personal list, that personal list takes priority.
- Treat `daytrading.monster` as a market-relevance candidate pool, not as a personal watchlist. Its useful fields are `market`, `code`, `name`, `theme`, `weight`, and `reason`; prefer higher `weight`, currently relevant `theme`, and names that match the earnings calendar.
- Do not mention DayTrading.monster, theme-data, candidate-source names, local paths, or other source boilerplate in Calendar titles/descriptions or final prose by default. If sources are requested, URLs may be included in a separate source/audit list.

## Earnings Workflow

### 1. Find Earnings Whispers And Verify The Calendar

- If the user provides an image, read it directly.
- If the user asks Codex to find the weekly earnings image, search the web instead of asking the user for the image.
- Prefer sources in this order:
  1. Reddit `r/EarningsWhisper` posts by `epswhispers`, because they are easy to search, usually have the image attached, and the post title often includes the exact week.
  2. Earnings Whispers website/calendar pages, useful for cross-checking dates/tickers but not always enough to recover the summary image.
  3. Reposts/image search only as fallback, and only if the image itself clearly shows the correct week.
- Do not use X by default. It often requires login or browser permissions and is not worth the friction for this workflow. Try `https://x.com/eWhispers` only if the user explicitly asks for X as the source.
- Useful search patterns:
  - `site:reddit.com/r/EarningsWhisper "The Most Anticipated Earnings Releases" "<Month D, YYYY>"`
  - `site:reddit.com/r/EarningsWhisper "week of <Month D, YYYY>" "epswhispers"`
  - `Earnings Whispers Most Anticipated Earnings Releases week beginning <Month D, YYYY>`
  - `Earnings Whispers earnings calendar <week Monday date>`
- Confirm the image or post title explicitly says the correct week, such as "Week of <Monday date>" or "week beginning <Monday date>". Do not use an image for the wrong week.
- If the date is unclear, keep searching or ask the user before writing events.

### 2. Extract And Normalize

- Extract tickers by weekday and release timing:
  - US before open
  - US after close
- Watch for OCR mistakes on small labels. Verify suspicious ticker labels against the user's watchlist CSV or a reliable ticker source. Example: Circle is `CRCL`, not `CRCI`.
- Map US session timing from `America/New_York` to the user's local timezone and account for US daylight saving time:
  - US before open -> `08:30 America/New_York`, duration 30 minutes, converted to the user's local timezone.
  - US after close -> `16:00 America/New_York`, duration 30 minutes, converted to the user's local timezone.
  - Do not hard-code JST examples unless the user's local timezone is Japan; show the converted local time only when useful.
- If Friday after-close is absent, do not invent it.

### 3. Prioritize Title Tickers

- For US stocks, default to the user's moomoo `美股` watchlist through the `us-stock-gamma-moomoo` skill/OpenD workflow, unless the user provides a more specific list for this task.
- If the user provides a watchlist CSV, use it as an ordered priority list. Detect common ticker columns such as `代码`, `Ticker`, `Symbol`, or similar. The earlier a ticker appears, the more important it is.
- If moomoo or CSV is unavailable, prioritize by market relevance: liquidity, market cap, options/retail attention, sector read-through, and user-stated preferences in the conversation.
- For US stocks, when no personal watchlist is available or the user asks for a broader candidate pool, use `daytrading.monster` theme data as the backup relevance source. Do not create events solely because a ticker appears there; require overlap with the earnings calendar and meaningful market relevance.
- Put only the tickers the user likely needs to see in the title, primarily watchlist matches.
- If a slot has no watchlist matches, do not create a Calendar event for that slot unless the user explicitly asks for every slot to be represented.
- When skipping a no-match slot, mention it in the final report with the session and the main tickers that were skipped, so the user can audit what was intentionally left out.
- Use a short fallback title with the most liquid/market-relevant names only when the user has no usable watchlist or explicitly wants a title for every slot.
- Keep all extracted tickers in the description.
- If an earnings slot overlaps with a macro or market-event calendar item, keep the earnings event separate instead of merging titles or descriptions.

### 4. Calendar Format

Title:

```text
🇺🇸 ER | TICKER TICKER TICKER
```

Description structure:

```text
重点看点：
・AAA：一句话写业务/交易看点和财报重点。
・BBB：一句话写业务/交易看点和财报重点。

其他留意：只写少量非标题但值得关注的名字和原因。
```

Do not include redundant blocks such as "美股时段", repeated timezone labels, or "标题重点" when the title and calendar slot already make them clear.

## Japan Earnings Workflow

### 1. Source And Scope

- Prefer SBI Securities settlement announcement data when available. The public ETGate page embeds the real Iris JSONP endpoints and volatile request parameters in inline JavaScript:
  - `ANNOUNCE_INFO_DATE`
  - `ANNOUNCE_INFO_PARAM`
  - `ANNOUNCE_CALENDAR_URL`
  - `ANNOUNCE_CALENDAR_PARAM`
- Do not call `vc.iris.sbisec.co.jp/calendar/settlement/stock/announcement_info_date.do` with only `selectedDate`; SBI returns `<!-- ERROR Calendar -->`. First fetch the current ETGate entry page, extract `ANNOUNCE_INFO_DATE` and `ANNOUNCE_INFO_PARAM`, then call `ANNOUNCE_INFO_DATE + ANNOUNCE_INFO_PARAM + "&selectedDate=YYYYMMDD"`.
- Query one selected date at a time; the JSONP response contains the full day's body and the website pagination is only front-end display. Do not scrape page-by-page if the JSONP endpoint is available.
- Use `selectedDate=YYYYMMDD` for each trading day in the requested week.
- A helper script is available at `scripts/fetch_sbi_jp_earnings.py`. Prefer it for direct SBI retrieval; it dynamically discovers the current API URL and hash/type parameter from the ETGate page.
- If the ETGate URL changes or the helper cannot extract the JavaScript variables, recover the current entry page by searching the web for `sbi 決算発表スケジュール` or `site:sbisec.co.jp 決算発表スケジュール 国内株式`, then use the discovered URL as the helper's `--entry-url`.
- If SBI is unavailable after dynamic discovery, use Traders Web `https://www.traders.co.jp/market_jp/earnings_calendar` as fallback. It is easy to parse but may require pagination.

### 2. Watchlist And Filtering

- For Japan stocks, default to `daytrading.monster` theme data with `market: "JP"` as the candidate list, unless the user provides a Japan CSV or another usable personal list.
- If the user provides a Japan stock CSV, add only matching stock codes from that CSV. Detect columns such as `代码`, `コード`, `Ticker`, or `Symbol`.
- Use the CSV order as priority. Earlier rows are more important and should appear first in titles and details.
- If the user says to use moomoo watchlists, read the relevant moomoo group(s) when available. If moomoo only returns Japan index futures or otherwise cannot provide individual Japan stock codes, say so and continue with `daytrading.monster` as the default candidate source.
- Never add every Japan earnings item by default. When a Japan CSV, moomoo-derived list, or `daytrading.monster` candidate list is being used, create Calendar events only for earnings names that overlap that list, unless the user explicitly asks to broaden beyond the list.
- After finding list overlaps, prioritize within those overlaps by CSV/list order, market cap, liquidity, index relevance, sector read-through, user preferences, and the `theme`/`weight`/`reason` fields from `daytrading.monster`.

### 3. Calendar Grouping

- Use the published Japan event time as the source time, then convert it to the user's local timezone before writing Calendar events.
- Group events by 30-minute bucket: `:00-:29` and `:30-:59`.
- Create one 0-minute event per bucket.
- If a stock has no concrete time, place it at `08:00` in the user's local timezone on that day, unless the user specifies another default.
- Disable reminders explicitly with `reminders: { use_default: false, overrides: [] }`.
- Prefer transparent events.

### 4. Title And Details

Title:

```text
🇯🇵決算｜会社名、会社名、会社名
```

- Use company short names after `決算｜`, not numeric stock codes.
- Keep only the highest-priority names in the title, usually up to 5. If more names are in the bucket, append `等N只`.
- Put stock codes in the description, not as the title's primary signal.

Description:

```text
具体时刻：
・会社名（コード，HH:MM）
・会社名（コード，HH:MM）

重点看点：
・会社名：一句话写业务/交易看点和财报重点。
・会社名：一句话写业务/交易看点和财报重点。
```

- Do not write redundant blocks like "时间分区", "标题重点", "本分区全部财报", or generic source disclaimers.
- Do not mechanically list `本決算`, forecast, or consensus for every stock. Mention estimates/consensus only when they are directly useful to the market note.
- The note should explain why the stock matters: business line, sector read-through, orders, margins, guidance, shareholder returns, FX sensitivity, AI/semiconductor exposure, bank net interest margin, defense orders, commodity price exposure, or similar.

## Macro/Event Workflow

### 1. Build The Weekly List

- Cover China, US, and Japan events that can move equity, rates, FX, commodities, crypto, or the user's watched stocks.
- Prioritize Japan because the user trades Japan most actively. Include Japan events that can realistically move JGB yields, USDJPY/JPY crosses, Japanese banks, exporters, growth stocks, real estate, semiconductors, or broad TOPIX/Nikkei risk appetite.
- Do not turn this into a generic economic calendar. If there are too many candidates, keep only the events that are tied to the current market theme and have a plausible trading impact.
- Always identify the current market theme before ranking events. Examples:
  - Japan inflation acceleration, BOJ hiking risk, and super-long JGB yield pressure.
  - US inflation/Fed repricing driving USDJPY and global growth stocks.
  - China policy or demand affecting Japan exporters, commodities, and Hong Kong/China equities.
- Raise the priority of events that match the current theme; lower or exclude events that are normally important but not relevant to the current trading narrative.
- Exclude categories the user already says they are handling separately, such as earnings or Treasury auctions.
- Include only events with enough confidence in date/time. Treat unconfirmed diplomacy or political headlines as an observation item unless there is recent official confirmation.
- For current or future event calendars, browse current sources. Build candidates from a mix of comprehensive economic calendars, Chinese market-weekly calendars, and official calendars:
  - Use comprehensive calendars such as ActionForex, Investing.com, Trading Economics, Myfxbook, ForexFactory, and similar sources to collect cross-country data releases, forecast/consensus, and prior values.
  - Use Chinese market-calendar and market-weekly sources such as Jin10 (`jin10.com` / `xnews.jin10.com`) and Wallstreetcn Calendar (`https://wallstreetcn.com/calendar`) to catch China/HK-market framing, geopolitics, oil/gold/inflation narratives, and events that may not surface clearly in official data calendars.
  - Prefer official release calendars for final confirmation of high-importance US/Japan/China event dates and times: Fed, US Treasury, BLS/BEA/Census, BOJ, Japan MOF, Japan Statistics Bureau, Cabinet Office, China NBS, PBOC/LPR, customs, and finance ministry sources when available.
  - Treat Jin10 and Wallstreetcn as candidate discovery and market-narrative inputs, not as the sole authority for critical times. Cross-check `★★★★` and `★★★★★` events against official or another high-quality calendar before writing to Google Calendar whenever possible.

### 2. Rank And Filter

- Assign importance stars from `★` to `★★★★★`.
- For Calendar writing, if the user asks for "四星以上", include only `★★★★` and `★★★★★`.
- Even when the user says "四星以上", do not add every `★★★★` event automatically. Add `★★★★` only when it is connected to the current market theme and has a clear impact path. Add all `★★★★★` unless there is no concrete time or the event is unconfirmed.
- Default to a smaller, higher-signal calendar. The goal is not coverage; the goal is to prevent noise while preserving events that can change trading decisions.
- Treat Japan inflation, BOJ communication, and JGB supply/demand events as high priority only when Japan rates/JPY are an active market driver. Examples include national CPI, Tokyo CPI, CGPI, BOJ decision/outlook/report, Summary of Opinions, BOJ minutes, Governor/deputy governor speeches, and 10y/20y/30y/40y JGB auctions.
- Require a concrete time for Calendar insertion unless the user explicitly wants all-day/undated watch items.
- Data releases use duration 0 minutes. Speeches or press conferences use duration 30 minutes unless the user specifies otherwise.

### 3. Required Details

For each event, collect or estimate:

- Importance stars.
- Forecast/consensus and prior value where available. If no reliable numeric consensus exists, say so.
- "If higher than expected" impact.
- "If lower than expected" impact.
- Make impacts concrete where possible: USD, JPY, CNH, yields, Nasdaq/growth stocks, value/cyclicals, gold, crypto, commodities, China/HK equities, Japanese banks/exporters.
- For Japan-relevant events, explicitly state the likely direction for JGB yields, JPY, and affected Japanese equity groups when applicable: banks, exporters, growth stocks, real estate, semiconductors, domestic demand, or commodities.

### 4. Calendar Format

Single event title:

```text
🇺🇸 美国4月CPI
🇨🇳 中国4月CPI/PPI
🇯🇵 BOJ Summary of Opinions
```

Combined title examples:

```text
🇺🇸 美国4月零售销售 / 进口价格
🇯🇵 日本PPI / BOJ发言
🇨🇳 中国CPI/PPI / 🇺🇸 美国CPI
```

Description structure:

```text
重要度：★★★★

预期/前值：
・预期：...
・前值：...

如果高于预期：
・利多/利空...

如果低于预期：
・利多/利空...
```

For combined events, repeat the same block per event separated by:

```text
---
```

Do not repeat the event name, country, type, or calendar time in the description when the title and calendar slot already show them. Keep the description focused on importance, forecasts, and directional market impact.

If a macro or market-event item overlaps with an earnings event, keep the macro/event item separate instead of merging titles or descriptions.

## Updating Existing Events

- For existing US Treasury auction events in the target week, title-prefix with `🇺🇸`.
- For existing `ER |` events, title-prefix with `🇺🇸` unless already present.
- For 5-star events, update `color_id` to `11` red.
- Do not add duplicate flags. If a title already begins with the correct flag, leave it.

## Verification

After writing:

- Search the target week for the created/updated title prefix or keyword.
- Confirm count, titles, dates/times, and color for 5-star items.
- Summarize only what changed and mention anything intentionally excluded, such as unconfirmed events or no concrete time.
