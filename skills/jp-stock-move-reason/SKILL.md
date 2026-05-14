---
name: jp-stock-move-reason
description: Use when analyzing why a Japanese stock moved sharply using Codex, without Gemini, from Yahoo Finance quote data, Yahoo 掲示板 comments, Yahoo/Kabutan/Traders news, and basic stock metrics such as current change, market cap, PER/PBR, dividend yield, and margin ratio.
metadata:
  short-description: Analyze Japanese stock move reasons from Yahoo掲示板, news, and metrics
---

# JP Stock Move Reason

Use this skill from the DTM repo root when the user asks why a specific Japanese stock is rising, falling, 急騰, 急落, 異動, or otherwise moving, and wants Codex to analyze it instead of Gemini.

The bundled script is safe to keep in a public repository: it uses only public web pages/APIs, does not read credentials, and does not call any LLM service.

## Workflow

1. Read `references/experience.md` before analysis, but only the `Active Playbook` and `Compression Protocol` sections unless the user explicitly asks for historical lessons. Apply those lessons when setting expectations, especially around earnings, guidance, valuation, 掲示板 sentiment, theme leadership, peer follow-through, and whether the stock is a leader, follower, defensive alternative, old-leader rebound, or noise.

2. Run the collector script from the repo root:

```bash
python3 skills/jp-stock-move-reason/scripts/stock_move_sources.py 7203 --format markdown
```

Useful options:

- `--hours 24`: evidence window. Use `72` when same-day materials are thin.
- `--comments 30`: maximum Yahoo 掲示板 comments to include.
- `--news-limit 15`: maximum news items to include.
- `--sources yahoo,kabutan,traders`: default news sources.
- `--market-hint 東証G`: improves Traders Web metric/news URL choice when known.

3. If network access fails in Codex, rerun the same command with sandbox escalation according to the normal approval policy.

4. Analyze the script output directly. Do not call Gemini. Treat sources with this priority:

- Current quote and basic metrics: establish whether there is a real price move and the stock's size/liquidity context.
- News: primary evidence for concrete catalysts.
- Yahoo 掲示板: secondary evidence for market psychology, rumors, expectations, and retail attention. Never treat it as confirmed fact unless the same item appears in news.
- Peer and theme reactions: use them to judge whether the move is theme-wide leadership, same-theme follow-through, or only stock-specific sentiment.

5. In multi-turn discussions about the same stock, treat user follow-ups as possible new evidence or feedback. If the user adds information, challenges the reasoning, asks for reconsideration, or the conversation reveals that the prior answer missed/misweighted something, re-evaluate the stock with the new context before defending the earlier answer.

6. If the analysis or multi-turn correction produces a durable reusable lesson, update experience after answering. First decide scope: if the lesson applies to both Japanese stocks and A-shares, update both stock-skill `references/experience.md` files; if it is specific to Japanese stocks, update only this skill. Follow the `Conversation Learning Protocol` and `Compression Protocol`: generalize the lesson, merge repeated lessons into the active summary, keep the active section short, and move only distinct older details into the archive.

## Output Style

Reply in Chinese unless the user asks otherwise. The answer can be detailed because this is a local script workflow: start from at least 3-4 lines, and when evidence is rich, write up to the length of a short market news note. Stay evidence-based.

For every stock analyzed, always use these five numbered sections in this exact order:

1. `最有力理由`: the most likely catalyst, with source names and timing.
2. `补助理由`: secondary drivers such as theme buying, short-term speculation, or market-cap/liquidity context.
3. `掲示板温度`: summarize heat level, recent post volume, and high-like comments.
4. `确定度`: high / medium / low, with one sentence explaining why.
5. `注意点`: what remains unconfirmed or what could invalidate the read.

When the user gives multiple stocks, write the five numbered sections separately for each stock first. After all individual stock sections, add a final comparison section such as `两只对比` or `多只对比`, covering common drivers, differences in catalyst quality, sentiment heat, and relative risk. You may add extra sections when useful, but the five required sections and the final comparison for multi-stock requests must remain present.

If the evidence is weak, say so plainly and use wording like `思惑`, `期待`, `传闻`, or `确认待ち`. Do not invent catalysts absent from the collected news/comments.

When explaining a catalyst, always check the expectation gap: `市场原来预期什么` -> `实际消息落地什么` -> `超预期 / 符合预期或只是落地 / 不及预期`. This applies to numeric news such as guidance, earnings, orders, dividends, and buybacks, and to qualitative news such as wording strength, timing, certainty, management confidence, regulatory tone, and whether the news solves the market's real concern.

## Valuation Requests

When the user asks for `合理估值`, `目标价`, `估值`, `贵不贵`, `空间`, `fair value`, or similar:

- Still collect current quote/news materials first, then add financial guidance, EPS/share-count, capital policy, and peer/sector context when available.
- Use the `Reasonable Valuation Framework` from `references/experience.md`.
- Provide scenario ranges rather than one exact target: conservative / base / bull.
- State the anchors used, such as forward EPS/PER, operating or recurring profit, ROE/PBR, EV/EBITDA, orders/backlog, buyback/CB dilution, and peer multiples.
- Explicitly say what the current price already prices in, what must happen to justify upside, and what would invalidate the valuation.
