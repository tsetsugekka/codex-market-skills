---
name: macro-news-check
description: Use when stock, index, gamma, or market analysis needs current macro or broad-market context from live news sources such as Jin10, Wallstreetcn, FinancialJuice, and market tape confirmation sources such as Sohu for A-share sector/index breadth and JPX for Japanese real-time index/sector strength. Especially useful for rates, FX, central banks, commodities, geopolitics, index moves, market-wide risk sentiment, sudden cross-asset news, A-share broad-market/sector rotation questions, or Japan market breadth/sector-drag questions.
---

# Macro News Check

Use this skill only when the analysis genuinely needs current macro, broad-market, or cross-asset context. Do not run it for every single-stock question by default.

This skill is public-safe: it uses public pages or feeds and must not store credentials, cookies, account data, private research paths, or raw copyrighted news dumps. Summarize only the headlines and implications needed for the user's market question.

## Trigger Conditions

Call this skill when one or more of these are true:

- The user asks about 大盘, 宏观, 利率, 汇率, 美债, 日债, 央行, CPI/PCE/FOMC/BOJ/ECB, commodities, oil, gold, geopolitics, or market-wide risk sentiment.
- A stock/index/ETF is moving with no clear stock-specific catalyst, or the move may be driven by rates, FX, futures, sector-wide risk, policy, or global headlines.
- Technical analysis needs a broad-market confirmation, especially for index breaks, high-beta stocks, export-sensitive Japanese names, A-share market emotion, US premarket moves, or same-day trading judgments.
- Gamma analysis would be unreliable without checking macro headlines, event risk, vol shock, index futures, yields, USD, or geopolitical tape risk.
- U.S. stock-move or gamma workflows such as `us-stock-move-reason` and `us-stock-gamma-moomoo` involve Fed expectations, rates, USD, oil/gold, index futures, market-wide risk appetite, or geopolitical shocks.
- A prior single-stock read may be missing a market-wide reason for a selloff or squeeze.

Do not call this skill when the request is clearly only about static fundamentals, historical valuation, company filings, or a chart level that does not depend on current market tone.

## Source Order

Prefer sources in this order, adjusting for language and market:

1. `Jin10` (`https://www.jin10.com/`): preferred Chinese macro tape when accessible. Its data quality is generally strong for real-time Chinese-language macro, central-bank, commodity, FX, and geopolitical headlines. The homepage can expose server-rendered flash items; the underlying flash API or WebSocket may require frontend headers/cookies and can be more fragile.
2. `Wallstreetcn` (`https://wallstreetcn.com/live/global`): useful Chinese backup and Asia/China market tape. If the page is a frontend shell, try its live JSON endpoint pattern:
   `https://api-one-wscn.awtmt.com/apiv1/content/lives?channel=global-channel&client=pc&limit=10`
3. `FinancialJuice` (`https://www.financialjuice.com/`): useful English global tape, especially US/EU macro, rates, FX, commodities, geopolitics, and market-moving headlines. Public RSS pattern:
   `https://www.financialjuice.com/feed.ashx?xy=rss`
   Tested shell fetch:
   `curl -L 'https://www.financialjuice.com/feed.ashx?xy=rss'`
   Quote the URL in zsh or other shells where `?` can be treated as a glob pattern. The feed returns broad global headlines; fetch the full feed first, then filter by macro relevance.

Use more than one source when the headline is important, surprising, or likely to change the market read. Prefer original official sources when a live headline points to a specific data release, central-bank statement, government notice, or company disclosure.

Do not use ticker or ETF keywords such as `SPY`, `QQQ`, `ES`, or a single stock symbol as the first-pass macro-news filter. Important macro drivers often appear under geopolitics, oil, rates, FX, central banks, fiscal policy, sanctions, shipping, elections, or official comments without mentioning the target instrument. First ingest the general live tape from the preferred sources; only then map relevant headlines to the user's instrument and confirm with market prices.

If a market report passes in pre-screened narrative-status entries, use them only as social-media-derived macro or theme candidates. Account/source quality can be treated as acceptable for screening, but timeliness is mandatory: the feed generation/review time and each entry's source/update time must fit the active market window. Fresh entries may guide what to verify in live macro tape and market prices; stale entries are background and must not be treated as current macro evidence.

Macro analysis must combine two live streams rather than treating either one as automatically superior:

- `News / event stream`: identify whether the market narrative or event state is changing. Focus on state changes, not isolated headlines: escalation vs de-escalation, tightening vs easing, supply shock vs supply relief, inflation impulse vs disinflation impulse, growth scare vs resilience, liquidity stress vs liquidity repair, and official confirmation vs rumor/trial balloon.
- `Market data stream`: check whether assets confirm, fade, or contradict the news. Use live or near-live prices for yields, FX, commodities, volatility, index futures, and local breadth where relevant.

Classify the relationship between the two streams before concluding:

- News confirms the price trend.
- Prices confirm a new headline shock.
- News is bad but prices refuse to fall.
- News is good but prices refuse to rise.
- Prices moved first and headlines are explaining the move late.
- Headlines changed but prices have not yet repriced.

Potential inflection points often appear when bad news no longer pushes risk assets lower, good news no longer lifts risk assets, yields stop rising despite inflationary headlines, oil stops rising despite supply-risk headlines, VIX stops expanding despite negative news, USD/JPY or DXY diverges from rates, high beta/Nasdaq leads while macro headlines remain scary, or defensive assets rise together with equities. This is only a candidate signal unless chart structure, recent price sequence, or intraday levels confirm it. Without enough chart/sequence context, describe it as news-price agreement or disagreement rather than a confirmed divergence or trend turn.

For intraday macro judgments, do not rely on headlines alone and do not rely on prices alone. Use headlines to detect narrative/state changes, use market prices to confirm or challenge them, and explicitly mention meaningful conflicts:

- Data-source priority for intraday macro prices:
  1. Official non-delayed / streaming price.
  2. Reputable non-official non-delayed price.
  3. Crypto/tokenized/perpetual-swap non-delayed proxy, clearly labeled as `链上` / `on-chain` / `proxy`.
  4. Official delayed price, with the delay stated.
- `DayTrading.monster` (`https://daytrading.monster/`) is a useful dashboard wrapper around TradingView widgets. Its default macro symbols include US index CFDs/futures, VIX, USD/JPY, DXY, US 10Y/30Y yields, gold, oil, copper, Nikkei CFD, TOPIX, Hang Seng, HK Tech, Taiwan, and Europe. If a futures, index, macro indicator, CFD, FX, commodity, or bond-yield code is unknown, check DayTrading.monster first and reuse its TradingView symbol. Symbols without the `D` badge can be used; `D` marks delayed exchange-limited data and should be avoided when a non-`D` alternative exists. A `24h` badge means the symbol is valid for 24-hour macro monitoring. A `365d` badge means the symbol is valid year-round. Blockchain/tokenized/perpetual-swap symbols can be used when they are the best non-delayed source under the priority order above, but every output must label them clearly as `链上`, `on-chain`, or `proxy`, rather than official underlying prices. The page itself is mostly a frontend shell; inspect its JavaScript or use the TradingView scanner equivalents when data must be read programmatically.
- TradingView scanner is the preferred programmatic fallback for live/near-live rates and cross-asset checks when accessible. Useful symbols include:
  - US yields: `TVC:US02Y`, `TVC:US10Y`, `TVC:US30Y`
  - Japan yields: `TVC:JP02Y`, `TVC:JP05Y`, `TVC:JP10Y`, `TVC:JP20Y`, `TVC:JP30Y`
  - US index futures: `CME_MINI:ES1!`, `CME_MINI:NQ1!`, `CBOT_MINI:YM1!`, `CME_MINI:RTY1!`
  - Vol, FX, commodities: `CBOE:VIX`, `TVC:DXY`, `OANDA:USDJPY`, `NYMEX:CL1!`, `ICEEUR:BRN1!`, `OANDA:XAUUSD`, `OANDA:XCUUSD`
  - Always inspect the returned `update_mode`. Some symbols are delayed even when they are easy to fetch. For example, `CBOE:VIX` is often `delayed_streaming_900`, while `ICEEUR:BRN1!` and `NYMEX:CL1!` are often `delayed_streaming_600`.
  - Prefer non-delayed official or conventional market symbols for intraday judgment. Tested examples: `TVC:VIX` is a streaming VIX indicator; `TVC:US10Y`, `TVC:US30Y`, and `TVC:JP30Y` are streaming yield indicators. For WTI/Brent, if no official or reputable non-official non-delayed source is available programmatically, use crypto/tokenized/perpetual-swap non-delayed proxies before official delayed reference prices, and label them clearly as `链上` / `on-chain` / `proxy`.
  - Crypto/tokenized/perpetual-swap proxies: `MEXC:USOILUSDT.P`, `HTX:USOILUSDT.P`, `BTCC:USOILUSDT.P`, `MEXC:UKOILUSDT.P`, `KCEX:BZUSDT.P`, `BINANCE:SPYUSDT.P`, and `BINANCE:QQQUSDT.P` can provide 365-day proxy signals. Use them before official delayed symbols only when no official/reputable non-official non-delayed source is available, and label them as proxies.
  - Not every DayTrading.monster TradingView widget symbol is available through scanner. If a preferred no-`D` dashboard symbol such as `CAPITALCOM:VIX` does not return through scanner, either read it visually from the dashboard or fall back to a scanner symbol and state its delay/proxy status.
- Eastmoney public endpoints or Eastmoney-related skills can often replace AkShare for China macro, China-US daily yield tables, global index tables, and commodity/futures confirmation. Use Eastmoney when it is not delayed and the timestamp/fields confirm freshness. Prefer direct Eastmoney requests when the endpoint is known, because this avoids Python dependency drift and makes failures easier to debug. Eastmoney does not normally require an API key for these public endpoints, but URLs/tokens can change and requests can be blocked or disconnected.
  - China-US Treasury daily yield table endpoint pattern used by AkShare:
    `https://datacenter.eastmoney.com/api/data/get?type=RPTA_WEB_TREASURYYIELD&sty=ALL&st=SOLAR_DATE&sr=-1&token=894050c76af8597a853f5b408b759f5d&p=1&ps=500&pageNo=1&pageNum=1`
  - Useful field mapping for that endpoint:
    - `SOLAR_DATE`: date
    - `EMM00588704`, `EMM00166462`, `EMM00166466`, `EMM00166469`: China 2Y, 5Y, 10Y, 30Y yields
    - `EMM01276014`: China 10Y-2Y spread
    - `EMG00001306`, `EMG00001308`, `EMG00001310`, `EMG00001312`: US 2Y, 5Y, 10Y, 30Y yields
    - `EMG01339436`: US 10Y-2Y spread
  - Treat Eastmoney daily yield tables as daily context, not intraday truth. Same-day US yield fields can lag or be blank before the source updates.
- `AkShare` is optional and should not be the default. It is a useful no-API-key wrapper when direct endpoints are inconvenient, but it can introduce heavy Python dependencies and environment conflicts. If it is used, install it in an isolated temporary environment, never into the base Anaconda/Python environment:
  `python3 -m pip install --target /private/tmp/akshare_test akshare "numpy<2"`
  then run with:
  `PYTHONPATH=/private/tmp/akshare_test PYTHONNOUSERSITE=1 python3 -c "import akshare as ak; ..."`
  Tested but secondary interfaces: `ak.bond_zh_us_rate()`, `ak.futures_global_spot_em()`, `ak.index_global_spot_em()`.

For A-share broad-market tape questions, use live headlines first, then use Sohu market data as an auxiliary confirmation layer:

- `https://q.stock.sohu.com/cn/zs.shtml` and `https://q.stock.sohu.com/zs/zs-2.html`: index map and broad market level.
- `https://q.stock.sohu.com/cn/bk.shtml`, plus board pages such as `https://q.stock.sohu.com/pl/pl-1631.html` for industries and `https://q.stock.sohu.com/pl/pl-1630.html` for concepts: sector/concept涨跌幅 and where funds are landing.
- `https://q.stock.sohu.com/cn/zdt.shtml`: historical涨跌停/breadth reference when judging market emotion.

Do not let Sohu board ranks replace the headline tape. Use快讯 to identify whether there is a policy, macro, liquidity, overseas, or sudden risk event; use搜狐板块涨跌幅 to validate whether the tape is actually being traded and whether the move is broad, narrow, or only a theme squeeze.

For Japan broad-market tape questions, use live headlines first, then use JPX real-time index data as an auxiliary confirmation layer:

- `https://www.jpx.co.jp/markets/indices/realvalues/index.html`: official JPX real-time index page; it updates listed index data about every minute during regular trading hours.
- `https://www.jpx.co.jp/market/indices/indices_stock_price3.txt`: JSON data used by the JPX page, including major indexes, TOPIX New Index Series, size indexes, TOPIX 33 sectors, TOPIX-17, style indexes, and market-type indexes.
- `https://www.jpx.co.jp/market/indices/indices_stock_price3.time.txt`: data timestamp in `YYYYMMDDHHMM`.

Do not treat Nikkei/TOPIX weakness as a single cause without checking JPX sector/index composition. Use快讯 to identify JGB yield, USD/JPY, BOJ/MOF, overseas tech, China/Korea/Taiwan spillover, commodity, or geopolitical drivers; use JPX sector/index strength to confirm whether pressure is concentrated in autos, banks, machinery, electronics, real estate/REIT, exporters, growth, small caps, or broad beta.

## Workflow

1. Define the macro question before fetching:
   - Is the issue rates, FX, index futures, commodities, geopolitics, policy, or broad risk appetite?
   - Which market matters most: China/A-shares, Japan, US, Europe, global commodities, or cross-asset?
2. Fetch the minimum needed recent items from both streams:
   - Start with Jin10 for Chinese macro tape if accessible.
   - Use Wallstreetcn's live endpoint for Chinese/Asia backup and market breadth context.
   - Use FinancialJuice RSS for English global confirmation and US/EU tape. In shell, use `curl -L 'https://www.financialjuice.com/feed.ashx?xy=rss'`; do not omit the quotes around the `?xy=rss` URL in zsh.
   - Check actual market prices before concluding that macro is better or worse intraday: US index futures, VIX, US yields, JGB yields, USD/JPY, DXY, oil, gold, and any directly relevant local index/sector breadth.
   - For rates-sensitive US or Japan market reads, prioritize live/near-live yield quotes (`TVC:US10Y`, `TVC:US30Y`, `TVC:JP05Y`, `TVC:JP10Y`, `TVC:JP20Y`, `TVC:JP30Y`) over stale article text. A headline that says yields are surging can be outdated if live yields have already pulled back.
   - Use AkShare only as an auxiliary source for daily yield history, China macro, China/overseas index tables, and commodity/futures confirmation. Do not use AkShare alone to decide whether US/Japan yields are improving or worsening intraday.
   - For A-share broad-market, sector rotation, "买什么方向", or "要不要入场" questions, also check Sohu indexes and industry/concept board涨跌幅 after the快讯 check.
   - For Japan broad-market, Nikkei/TOPIX weakness, sector drag, or Japanese single-stock move with strong market pressure, also check JPX real-time indexes and TOPIX sector/TOPIX-17 strength after the快讯 check.
3. Identify whether the active narrative has changed:
   - Separate routine headlines from true state changes.
   - Ask what the market was previously pricing, what changed, and which asset chain should transmit the change.
   - Common transmission chains include: event risk -> oil/commodities -> inflation expectations -> long yields -> equity duration; central-bank repricing -> front-end yields -> FX -> equity multiples; growth data -> cyclicals/commodities -> index breadth; fiscal/debt concern -> long yields -> currency/volatility.
4. Compare news and prices:
   - If headlines and prices agree, classify it as trend confirmation.
   - If headlines are stale and prices already moved, avoid double-counting the same information.
   - If headlines changed but prices have not repriced, say whether the market may be ignoring the risk or waiting for confirmation.
   - If prices reject the headline direction, treat that rejection as evidence to investigate, not as a standalone reversal signal. Only discuss divergence, exhaustion, or a turn when recent chart structure, intraday sequence, or key levels support it.
5. Filter aggressively:
   - Keep only headlines that can plausibly affect the instrument being analyzed.
   - Prioritize timestamps, source type, affected asset class, and whether the item is data, policy, rumor, geopolitical, or routine noise.
6. Classify the macro effect:
   - `risk-on`: supports equities/high beta/cyclical trades.
   - `risk-off`: pressures equities/high beta; supports bonds, USD, defensive assets, or safe havens depending on context.
   - `rates-up pressure`: bad for long-duration growth, high valuation, weak balance sheets, bond proxies.
   - `rates-down support`: can help duration/growth, but check whether rates are falling from recession fear.
   - `FX-driven`: important for exporters, import-cost names, commodities, and ADR/local-market conversions.
   - `commodity shock`: sector-specific tailwind/headwind.
   - `policy/liquidity`: judge size, timing, credibility, and whether it is already expected.
7. Connect the macro tape to the specific analysis:
   - State whether macro is the main driver, a secondary amplifier, or only background noise.
   - Separate stock-specific catalysts from market-wide pressure.
   - Explain expectation gap: what the market likely expected, what the headline/data changed, and whether it was above, in line with, or below expectations.
   - For A-share盘面, state whether搜狐板块涨跌幅 confirms the快讯 narrative, contradicts it, or shows only a narrow局部行情.
   - For Japan盘面, state whether JPX sector/index strength confirms the快讯 narrative, contradicts it, or shows that the weakness is concentrated in a few heavyweight sectors.

## Output Style

Keep the macro section concise unless the user asks for a full macro brief. Use this structure when helpful:

1. `宏观结论`: one sentence on whether the tape is risk-on, risk-off, rates/FX-driven, or neutral.
2. `关键消息`: 2-5 relevant headlines with source and time when available.
3. `对标的影响`: how those headlines affect the stock/index/option map being analyzed.
4. `权重`: main driver / secondary amplifier / background only.
5. `需要确认`: what would require a fresh check, original source, or later market reaction.

When answering macro or broad-market tape questions, absorb the source material into analysis instead of mechanically narrating the data-gathering process. Do not mention aggregator or retransmission-site names such as Jin10, Wallstreetcn, FinancialJuice, Sohu, JPX, or TradingView in the final answer by default. If a live item cites an original outlet, official source, company disclosure, or named primary reporter/source, it is acceptable to mention that original attribution when it improves credibility or explains confidence, e.g. Bloomberg, Reuters, The Information, Nikkei, Axios, WSJ, CNBC, an official ministry/central bank/company statement, or a company filing. Mention aggregator names, timestamps, or URLs only when the user asks for sources, a fact is disputed, freshness needs auditing, or attribution materially changes confidence. Avoid repetitive phrasing such as "`快讯显示`", "`消息面显示`", "`搜狐确认`", or "`JPX 11:02 数据显示`" as sentence starters. Lead with the inferred market structure: what is driving, what is dragging, what funds are buying/selling, whether the move is broad or narrow, and what that means for the user's decision.

Do not paste long article text or bulk live-feed items. Paraphrase and cite only the short headline-level evidence needed for the analysis.
