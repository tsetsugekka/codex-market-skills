---
name: market-calendar-google
description: Organize a selected week of US earnings calendars or China/US/Japan macro and market-event calendars, prioritize what matters to the user, and add the resulting events to Google Calendar. Use when the user asks to handle this week's or next week's earnings, Earnings Whispers images, US stock ticker earnings, Treasury auctions, central-bank/data releases, or China/US/Japan financial events and wants them written to Google Calendar. Also use to view, save, revise, or remove local calendar preferences, including event-summary style.
---

# Market Calendar Google

先按[运行环境能力](references/runtime-capabilities.md)确认当前可用工具；下文工具与脚本流程在能力和授权具备时执行，不按宿主名称删减研究方法。

开始分析前，按[公共与私密 Reference 双读契约](references/reference-layers.md)读取本任务相关的公共与已获授权的私密 reference；两层均适用时都要读。

## Overview

Use this skill to turn weekly market calendars into concise Google Calendar events for the user. Support three workflows:

1. US earnings calendar for a week, usually from the Earnings Whispers "Most Anticipated Earnings Releases" image.
2. China/US/Japan macro, central-bank, auction, and market-event calendar for a week.
3. Japan stock earnings calendar for a week, usually from SBI Securities settlement announcement data.

Default to the user's local timezone from the runtime environment. Use the current date and timezone from the environment to resolve "this week" and "next week". If the user's timezone is unavailable, ask for the target timezone before writing Calendar events.

## Local Preference Reference

- Keep two layers: public references contain shared calendar methods and ship with the Skill; a separate private reference contains each user's own preferences and stays on that user's machine. Maintain both; do not turn the public references into a personal preference file.
- When the user asks to remember a preference for future calendars, or to view, revise or remove one, use this local-reference workflow. Preference-only requests need filesystem access, not Google Calendar access. A one-off instruction applies to the current task without becoming a saved default.
- Read the private index through the reference contract above and reuse the calendar preference document it maps. If no mapping exists, create `calendar-preferences.md` beside that index and register it under `market-calendar-google`; when no index exists, initialize it at the contract's default location. Keep both outside the public repository and installed Skill/plugin directories. If local files are unavailable, provide the proposed text and report that it was not saved.
- Save only the user's stated preference, its scope and update date; name the public section it overrides when applicable. Supported preferences include summary length/structure, content to emphasize or omit, language, title style, event selection, destination calendar and reminders. Do not invent values for unspecified preferences or store temporary market forecasts as preferences.
- Update the matching entry in place, preserving unrelated preferences. A clear new permanent choice replaces its prior value; a temporary override leaves the saved default intact. Remove only the requested preference. Ask only when the intended scope or replacement is unclear.
- On calendar tasks, apply the current request first, then applicable saved preferences, then public defaults, subject to the reference contract's truthfulness and permission boundaries. Saving preferences does not itself create, migrate or rewrite Calendar events.
- Read back the changed entry and index mapping, then briefly confirm what was saved, revised or removed. Local preference content and private identifiers stay out of public Skill source, GitHub and release packages.

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
- If the user specifies an existing calendar, call `list_calendars` and resolve exactly one `calendar_id`; if the name is missing or ambiguous, ask before writing. If no calendar is specified, use `primary`. Use that same `calendar_id` for the target-week duplicate search, every write, and the bounded post-write verification. Do not hard-code a private calendar ID or assume calendar create/move capabilities.
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
- For US earnings, the default personal watchlist source is the user's moomoo watchlist via the `us-stock-gamma-moomoo` skill/OpenD workflow. If it is unavailable or incomplete, `https://daytrading.monster/api/themes?market=us` may be used as the backup candidate theme list.
- For Japan earnings, the default candidate list source is `https://daytrading.monster/api/themes?market=jp`, because local moomoo OpenD may not expose individual Japan stock watchlist codes. If the user provides a Japan CSV or another usable personal list, that personal list takes priority.
- Treat `daytrading.monster` as a market-relevance candidate pool, not as a personal watchlist. Use the canonical JSON interfaces in `https://daytrading.monster/api-docs/` only; do not scrape the `/themes/` frontend HTML, `noscript`, or static SEO text as candidate data. Read `themes[]` (`market`, `theme_key`, `theme_name_zh`) and their `constituents[]` (`code`, `name`, `weight`, `reason_zh`); prefer higher `weight`, currently relevant themes, and names that match the earnings calendar. Parse the `text/plain` response body as JSON; it supplies candidates, not earnings dates.
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
- Resolve each company's release time before grouping: current-period official release time first; otherwise a dated, reliable earnings source's specific time; otherwise the session anchors below. Keep earnings release and investor call separate. An overseas issuer/ADR may release on its home-market clock; a US listing does not make its release a US-session event.
- Convert the dated source time with its IANA timezone and daylight-saving rules. If a timezone abbreviation conflicts with the local seasonal offset, cross-check a second timezone/UTC equivalent or a dated schedule and record the resolution; unresolved conflicting times remain unresolved, not an invented `08:00` placeholder.
- Only when the source gives a session without a specific release time, use these planning anchors from `America/New_York`, labelled as session anchors rather than confirmed release times:
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
- Keep all extracted tickers for each represented source slot in the description; distinguish title/watchlist priorities from other names. Do not move another company to a priority company’s precise release time merely because both were in the same source session.
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
- Use its JSON output to retain both `time` and `order_time`. [SBI's schedule notes](https://www.sbisec.co.jp/ETGate/?_ActionID=DefaultAID&_ControlID=WPLETmgR001Control&_DataStoreID=DSWPLETmgR001Control&_PageID=WPLETmgR001Mdtl20&burl=iris_economicCalendar&cat1=market&cat2=economicCalender&dir=tl1-cal%7Ctl2-schedule%7Ctl3-stock%7Ctl4-calsel&file=index.html&getFlg=on) say its displayed earnings `HH:MM` generally references the prior-year same-period TDNet release time, with exceptions such as newly listed stocks; it is not confirmation of this period's official release time. When an exchange release date is unavailable, SBI may also use the prior-year same-period date mapped into the current year's calendar; treat that current-period date as expected.
- If the ETGate URL changes or the helper cannot extract the JavaScript variables, recover the current entry page by searching the web for `sbi 決算発表スケジュール` or `site:sbisec.co.jp 決算発表スケジュール 国内株式`, then use the discovered URL as the helper's `--entry-url`.
- If SBI is unavailable after dynamic discovery, use Traders Web `https://www.traders.co.jp/market_jp/earnings_calendar` as fallback. It is easy to parse but may require pagination.

### 2. Watchlist And Filtering

- For Japan stocks, default to the canonical `https://daytrading.monster/api/themes?market=jp` JSON as the candidate list, unless the user provides a Japan CSV or another usable personal list. Do not use rendered/static `/themes/` page text or `noscript` content for the candidate list.
- If the user provides a Japan stock CSV, add only matching stock codes from that CSV. Detect columns such as `代码`, `コード`, `Ticker`, or `Symbol`.
- Use the CSV order as priority. Earlier rows are more important and should appear first in titles and details.
- If the user says to use moomoo watchlists, read the relevant moomoo group(s) when available. If moomoo only returns Japan index futures or otherwise cannot provide individual Japan stock codes, say so and continue with `daytrading.monster` as the default candidate source.
- Never add every Japan earnings item by default. When a Japan CSV, moomoo-derived list, or `daytrading.monster` candidate list is being used, create Calendar events only for earnings names that overlap that list, unless the user explicitly asks to broaden beyond the list.
- After finding list overlaps, prioritize within those overlaps by CSV/list order, market cap, liquidity, index relevance, sector read-through, user preferences, and the `theme_key`/`weight`/`reason_zh` fields from `daytrading.monster`.

### 3. Calendar Grouping

- Use the current period's expected release date in the selected week. A historical reference date must not replace that date; keep the date's expected/confirmed status separate from the time's status.
- Use SBI's selected-week date and available `HH:MM` directly as the expected schedule. Do not research each company's official IR time first: historical reference times are sufficient for this calendar's planning purpose. Consult official IR only for a user-requested check or a concrete conflicting schedule already found; record any resulting override.
- Extract `HH:MM` from values such as `15:40 (予定)` or `15:40:00`; retain the reference/expected status in the description.
- Combine the current period's release date with the chosen source time in `Asia/Tokyo`, then convert the date and time to the user's local timezone before grouping or writing Calendar events.
- Group events by 30-minute bucket: `:00-:29` and `:30-:59`.
- Create one 0-minute event per bucket.
- When SBI has no usable time, use an already-established override if available; otherwise place the stock at `08:00` in the user's local timezone on the current period's expected release date, unless the user specifies another default; label it as a time-unannounced placeholder.
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
排程时刻：
・会社名（コード，HH:MM；SBI参考／预计）

重点看点：
・会社名：一句话写业务/交易看点和财报重点。
・会社名：一句话写业务/交易看点和财报重点。
```

- Do not write redundant blocks like "时间分区", "标题重点", "本分区全部财报", or generic source disclaimers.
- Briefly label each stock’s time as `SBI参考／预计`, an explicitly verified override, or a time-unannounced placeholder. No repeated official-confirmation disclaimer or historical-period research is needed.
- Do not mechanically list `本決算`, forecast, or consensus for every stock. Mention estimates/consensus only when they are directly useful to the market note.
- The note should explain why the stock matters: business line, sector read-through, orders, margins, guidance, shareholder returns, FX sensitivity, AI/semiconductor exposure, bank net interest margin, defense orders, commodity price exposure, or similar.

## Macro/Event Workflow

### 1. Discover Before Filtering

Build the candidate set before assigning stars. A short final calendar requires broad discovery; it is not evidence of complete research by itself. Search the whole requested week, including weekend decisions and releases that cross local midnight.

Cover the requested China, US and Japan markets, prioritizing Japan when that is the user's trading focus. Identify the user's markets and active themes from current evidence. Use them to prioritize, not to exclude contrary catalysts or events that could change the theme. Respect categories the user explicitly handles separately.

Cover these complementary source roles in the first pass, without waiting for the user to supply a weekly article:

| Role | Starting sources | What to capture |
| --- | --- | --- |
| Scheduled macro baseline | A comprehensive calendar such as Investing.com, Trading Economics, ActionForex or ForexFactory | Data, central banks, auctions, prior values and dated consensus |
| Weekly catalyst discovery | The target week's Wallstreetcn “下周重磅日程” or Jin10 weekly outlook; a Japanese weekly outlook/calendar such as public Nikkei, Kabutan or a major Japanese broker | Policy deadlines, industry events, product launches, monthly operating data, holidays and market structure |
| Authoritative confirmation | Relevant agency, central bank, exchange, company IR, organizer or producer-group schedule | Event identity, status, date, timezone, release versus conference-call time |

Use independent coverage, not multiple mirrors of one article. Official calendars confirm known events well but do not discover all cross-industry catalysts. Search company/organizer schedules for the active themes that broad calendars do not cover. If a source is unavailable, use an accessible equivalent and record the resulting gap; do not silently treat an inaccessible article as reviewed.

Confirm material candidates against the relevant official schedule or another high-quality independent source before insertion. Use Fed/Treasury/BLS/BEA for US releases, BOJ/MOF/Statistics Bureau for Japan, and NBS/PBOC/customs for China; use company IR, organizers, exchanges and OPEC for their respective events. Unconfirmed policy or political claims remain observation items.

Read complete weekly articles, every embedded calendar image/table and captions, whether discovered independently or supplied by the user. A headline, search snippet or text-only extract is insufficient when images contain additional events. Follow source-access and rate-limit rules of the current environment.

Check all four event classes below across the relevant transmission paths:

- Rates, FX and liquidity: policy communication, debt supply, reserve/liquidity operations, including foreign central banks when they affect the user's currencies or assets.
- Demand and earnings chain: China demand, trade and industrial profits; semiconductor exports, monthly revenue or production updates that inform watched suppliers/customers.
- Industry and company catalysts: AI/semiconductor, energy, automotive or other active themes; conferences, product availability and investor days with a concrete decision variable.
- Policy and market structure: implementation dates, tariff/export-control deadlines, index/expiry flows, ex-dividend dates, holidays and cross-border trading availability; include energy supply meetings and weekend decisions when material.

These are coverage checks, not mandatory calendar entries. For each relevant class, record candidates found or that a suitable source was checked with no material candidate; “not searched” is different from “none found.”

Maintain a compact working candidate ledger: event; discovery/confirmation source and as-of date; source-local date/time and timezone; affected assets and causal path; importance and confirmation status; include / already present / exclude with reason / unresolved. Keep account identifiers and private watchlists out of public artifacts. Use the ledger to compare the full candidate set against the existing calendar before writing.

### 2. Classify Before Ranking

Classify each candidate so that its evaluation and Calendar treatment are consistent:

1. **Systemic macro**: employment, inflation, growth, central-bank decisions, central-bank communication, and sovereign-auction supply/demand.
2. **Market structure**: index rebalances, expiry/settlement, inclusion changes, lock-up expiries, and scheduled trading-rule changes.
3. **Theme/company catalyst**: confirmed AI, semiconductor, energy, automotive, battery, or other industry conferences; product launches; and investor days. Earnings remain a separate workflow.
4. **Policy/geopolitical catalyst**: confirmed policy implementation, tariff deadlines, official meetings, or diplomacy with a clear asset-price transmission path.

Exclude vague commentary, routine sector events, one-off company items without a user-relevant read-through, and unconfirmed political headlines. Keep skipped candidates in the final audit only when that helps the user understand an intentional omission.

### 3. Rank And Filter

- Assign importance stars from `★` to `★★★★★`.
- For Calendar writing, if the user asks for "四星以上", include only `★★★★` and `★★★★★`.
- Even when the user says "四星以上", do not add every `★★★★` event automatically. Add `★★★★` only when it is connected to the current market theme and has a clear impact path. Include confirmed `★★★★★` under the timing rules below; keep unresolved events visible in the working ledger.
- Keep the written calendar selective after coverage is checked. Do not use a target event count or “avoid noise” as a reason to skip candidate discovery.
- Assess materiality from price impact, scope to change the next days/weeks outlook, connection to the user's assets, and surprise potential. Assess event confirmation and time precision separately: an important event with an unknown hour belongs in unresolved/eligible date-marker handling, not automatically in the low-importance bucket.
- For a four-star theme event, name the actual new information expected and the asset or supply-chain exposure it could reprice. A generic “AI benefits semiconductors” sentence does not establish materiality. Apply the same test to follow-up additions; the user's article and a larger addition count are not ground truth.
- An event's country, organizer size, lack of a conventional economic-calendar star, or absence from the personal stock list is not by itself a reason to reject a macro/industry catalyst. Show the read-through before deciding; preserve the user's separate earnings watchlist filter and disclose material excluded bellwethers when relevant.
- A `★★★★` entry needs both a clear transmission path and a current-theme connection. `★★★★★` is reserved for systemic catalysts or unusually sensitive Japan rates/JPY events. A headline's own star label is a discovery hint, not the final rating.
- Treat Japan inflation, BOJ communication, and JGB supply/demand events as high priority only when Japan rates/JPY are an active market driver. Examples include national CPI, Tokyo CPI, CGPI, BOJ decision/outlook/report, Summary of Opinions, BOJ minutes, Governor/deputy governor speeches, and 10y/20y/30y/40y JGB auctions.
- Require a concrete time for normal Calendar insertion. For a confirmed, high-signal conference, product launch, or policy meeting with no public time, use a transparent 0-minute `08:00` local-time marker only when the user's established preference permits it; state that the precise time is unannounced. For multi-day events, create one marker on the first day and include the date span in the title.
- Convert the source-market date and time into the user's local timezone. For a cross-timezone event with only a local date, try to confirm the actual start time before choosing the local Calendar date; do not silently present an uncertain conversion as an exact appointment.
- Data releases use duration 0 minutes. Speeches or press conferences use duration 30 minutes unless the user specifies otherwise.

### 4. Required Details

For each event, collect or estimate:

- Importance stars.
- Forecast/consensus and prior value where available. If no reliable numeric consensus exists, say so.
- "If higher than expected" impact.
- "If lower than expected" impact.
- Make impacts concrete where possible: USD, JPY, CNH, yields, Nasdaq/growth stocks, value/cyclicals, gold, crypto, commodities, China/HK equities, Japanese banks/exporters.
- For Japan-relevant events, explicitly state the likely direction for JGB yields, JPY, and affected Japanese equity groups when applicable: banks, exporters, growth stocks, real estate, semiconductors, domestic demand, or commodities.
- For central-bank officials’ speeches, label the person’s established policy reputation beside their name (usually hawkish / leaning hawkish / neutral / leaning dovish / usually dovish). The label describes the speaker, not the scheduled speech. Note a recent shift only when it materially changes that established impression. Reuse reliable evidence collected for the calendar, note its period in the description when needed, and use “unclear” if unsupported. This is background, not a prediction of the upcoming speech; do not turn a rough reference label into exhaustive research.
- For confirmed non-numeric events, replace forced forecast fields with the decision variables that matter: for example production guidance and commercialisation for a product launch, policy language and export controls for a government meeting, or supply guidance for OPEC+.
- Before replacing a forecast, match the indicator, period, units and survey timestamp, and distinguish market consensus from an institution's estimate. Newer publication alone is not stronger evidence. Resolve text/image conflicts with the underlying source where possible; otherwise label the disagreement and do not promote it to a single consensus or an invented consensus range. Update the existing event only when the revised value is supported; use the official release for prior/revised actuals.

### 5. Calendar Format

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

For earnings, reconcile unique company codes as well as grouped Calendar events. Record the week/source coverage, selected-list overlap, included codes and intentional exclusions; a small event count alone does not prove missing companies. Compare every included company's source date/time, time status (official / secondary schedule / SBI reference / session anchor / unknown), source timezone, converted time and bucket against the proposed event. Inspect every `08:00` placeholder for an available source time. After writing, read back actual event starts and company details against this ledger, not merely the write response or total count.

When correcting a recurring error, identify the Skill source/revision actually loaded and compare the relevant rule with the maintained source. For recurring runs, inspect the actual scheduled-task prompt as well as its Skill/read entrypoint for obsolete or conflicting rules, and verify authorized updates by reading both back; changing this week's events or a GitHub file alone does not establish that another runtime loaded the update. Keep deployment receipts and personal cases private.

Before writing, compare the candidate ledger with the proposed calendar by event class and source role. Revisit excluded high-impact candidates and unresolved timing, and check whether a Japanese trader's rates/FX, demand, industry and market-structure exposures have a blind spot. If relevant coverage remains unavailable, report the specific gap instead of claiming full coverage. Do not create marginal entries to fill an empty class.

After writing:

- Search the target week for the created/updated title prefix or keyword.
- Confirm count, titles, dates/times, and color for 5-star items.
- Confirm the date conversion for events sourced outside the user's timezone and the `08:00` placeholder convention for confirmed undated events.
- For Japan earnings, verify the current-period release date, official IR / SBI reference / placeholder time status, timezone conversion and 30-minute grouping; an available SBI historical reference time must not become `08:00` merely because it is not officially confirmed.
- Summarize only what changed and mention anything intentionally excluded, such as unconfirmed events, weak read-through, or unresolved timing under the relevant workflow. Japan earnings with usable SBI reference times remain eligible under their scheduling rule.

For a later supplement, distinguish a first-pass omission, genuinely new announcement, forecast/time revision and a change in user scope. Calendar entry counts differ from underlying event counts because of grouping; use the reviewed candidate ledger, not raw additions, to assess first-pass misses. Verification of successful writes does not establish research completeness.
