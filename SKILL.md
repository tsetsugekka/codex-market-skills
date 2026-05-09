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

Default timezone is `Asia/Tokyo`. Use the current date and timezone from the environment to resolve "this week" and "next week".

## Shared Rules

- Use Google Calendar tools. Search the target week first to avoid duplicates before creating or updating events.
- Preserve existing user-created calendar details unless the user asks to overwrite them.
- Put a country flag at the start of titles when the event has a clear country:
  - US: `🇺🇸`
  - China: `🇨🇳`
  - Japan: `🇯🇵`
- If several events fall in the same 30-minute bucket, combine them into one event. Buckets are `:00-:29` and `:30-:59`.
- If combined events are all from the same country, use the flag only once. If countries differ, include each relevant flag before its event name.
- Use Japanese-time event times in Calendar. In descriptions, write in Chinese unless the user asks otherwise.
- For 5-star events, set Google Calendar event color to red (`color_id: "11"` after confirming colors if needed).
- Prefer transparent events for informational market calendar items unless the existing event uses a different setting or the user asks to block the calendar.
- Do not include process/source boilerplate such as "parsed from image", local file paths, or explanations of why something was included. Include actionable market notes instead.
- Do not repeat information that is already obvious from the calendar title or time slot. For example, avoid writing "title focus", "Japan time", session labels, or the same event list twice unless that detail adds new useful context.

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
- Map US session timing from `America/New_York` to `Asia/Tokyo` and account for US daylight saving time:
  - US before open -> `08:30 America/New_York`, duration 30 minutes, converted to Japan time.
  - US after close -> `16:00 America/New_York`, duration 30 minutes, converted to Japan time.
  - During US daylight time this is usually `20:30 JST` before open and `05:00 JST` next day after close.
  - During US standard time this is usually `22:30 JST` before open and `06:00 JST` next day after close.
- If Friday after-close is absent, do not invent it.

### 3. Prioritize Title Tickers

- If the user provides a watchlist CSV, use it as an ordered priority list. Detect common ticker columns such as `代码`, `Ticker`, `Symbol`, or similar. The earlier a ticker appears, the more important it is.
- If no watchlist CSV is provided, prioritize by market relevance: liquidity, market cap, options/retail attention, sector read-through, and user-stated preferences in the conversation.
- Put only the tickers the user likely needs to see in the title, primarily watchlist matches.
- If a slot has no watchlist matches, use a short fallback title with the most liquid/market-relevant names only when the user wants a title for every slot.
- Keep all extracted tickers in the description.

### 4. Calendar Format

Title:

```text
🇺🇸 ER | TICKER TICKER TICKER
```

Description structure:

```text
重点看点：
- AAA：一句话写业务/交易看点和财报重点。
- BBB：一句话写业务/交易看点和财报重点。

其他留意：只写少量非标题但值得关注的名字和原因。
```

Do not include redundant blocks such as "美股时段", "日本时间", or "标题重点" when the title and calendar slot already make them clear.

## Japan Earnings Workflow

### 1. Source And Scope

- Prefer SBI Securities settlement announcement data when available. The public page loads JSONP from `vc.iris.sbisec.co.jp/calendar/settlement/stock/announcement_info_date.do`.
- Query one selected date at a time; the JSONP response contains the full day's body and the website pagination is only front-end display. Do not scrape page-by-page if the JSONP endpoint is available.
- Use `selectedDate=YYYYMMDD` for each trading day in the requested week.
- If SBI is unavailable, use Traders Web `https://www.traders.co.jp/market_jp/earnings_calendar` as fallback. It is easy to parse but may require pagination.

### 2. Watchlist And Filtering

- If the user provides a Japan stock CSV, add only matching stock codes from that CSV. Detect columns such as `代码`, `コード`, `Ticker`, or `Symbol`.
- Use the CSV order as priority. Earlier rows are more important and should appear first in titles and details.
- If the user does not provide a Japan stock CSV or similar watchlist, have the AI select a small set of important names by market cap, liquidity, index relevance, sector read-through, and user preferences. Never add every Japan earnings item by default.

### 3. Calendar Grouping

- Use Japan local time directly.
- Group events by 30-minute bucket: `:00-:29` and `:30-:59`.
- Create one 0-minute event per bucket.
- If a stock has no concrete time, place it at `08:00 Asia/Tokyo` on that day.
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
- 会社名（コード，HH:MM）
- 会社名（コード，HH:MM）

重点看点：
- 会社名：一句话写业务/交易看点和财报重点。
- 会社名：一句话写业务/交易看点和财报重点。
```

- Do not write redundant blocks like "时间分区", "标题重点", "本分区全部财报", or generic source disclaimers.
- Do not mechanically list `本決算`, forecast, or consensus for every stock. Mention estimates/consensus only when they are directly useful to the market note.
- The note should explain why the stock matters: business line, sector read-through, orders, margins, guidance, shareholder returns, FX sensitivity, AI/semiconductor exposure, bank net interest margin, defense orders, commodity price exposure, or similar.

## Macro/Event Workflow

### 1. Build The Weekly List

- Cover China, US, and Japan events that can move equity, rates, FX, commodities, crypto, or the user's watched stocks.
- Exclude categories the user already says they are handling separately, such as earnings or Treasury auctions.
- Include only events with enough confidence in date/time. Treat unconfirmed diplomacy or political headlines as an observation item unless there is recent official confirmation.
- For current or future event calendars, browse current sources. Prefer official release calendars for US/Japan/China data when available; use reputable economic calendars and news sources for consensus.

### 2. Rank And Filter

- Assign importance stars from `★` to `★★★★★`.
- For Calendar writing, if the user asks for "四星以上", include only `★★★★` and `★★★★★`.
- Require a concrete time for Calendar insertion unless the user explicitly wants all-day/undated watch items.
- Data releases use duration 0 minutes. Speeches or press conferences use duration 30 minutes unless the user specifies otherwise.

### 3. Required Details

For each event, collect or estimate:

- Importance stars.
- Forecast/consensus and prior value where available. If no reliable numeric consensus exists, say so.
- "If higher than expected" impact.
- "If lower than expected" impact.
- Make impacts concrete where possible: USD, JPY, CNH, yields, Nasdaq/growth stocks, value/cyclicals, gold, crypto, commodities, China/HK equities, Japanese banks/exporters.

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
事件：事件名称
类型：数据发布/讲话/央行文件/拍卖/政治财经事件
重要度：★★★★

预期/前值：
- 预期：...
- 前值：...

如果高于预期：
- 利多/利空...

如果低于预期：
- 利多/利空...
```

For combined events, repeat the same block per event separated by:

```text
---
```

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
