---
name: stock-sentiment-analysis
description: Reusable public-safe sentiment and market-emotion framework for A-shares, Japanese stocks, US stocks, indexes, and sector themes. Use when a stock or market move needs emotion-cycle classification, main-line versus follower judgment, expectation-gap analysis, forum/news sentiment synthesis, risk-on/risk-off context, or when other stock skills need a shared sentiment layer. Supports optional user-specified private RAG folders without storing or publishing private materials.
metadata:
  short-description: Reusable stock sentiment and emotion-cycle framework
---

# Stock Sentiment Analysis

Use this skill as the shared sentiment layer for market skills. It does not fetch data by itself; it tells Codex how to interpret evidence gathered by `cn-stock-move-reason`, `jp-stock-move-reason`, `stock-technical-analysis`, `us-stock-gamma-moomoo`, public news, forums, breadth, and user-provided screenshots or notes.

This public-safe skill must not contain personal information, API keys, account data, private paths, raw screenshots, full copied notes, ticker-specific personal trade logs, or proprietary labels from a private RAG corpus. It must remain usable without any private RAG folder.

## Public And Private Versions

If both public and private versions of a market skill exist, prefer the private version for local analysis when the user permits it. Use this public skill as the public-safe shared framework and as the release checklist source.

When updating a paired private/public skill, write public-safe generalized lessons to both versions, but keep private paths, private labels, raw notes, screenshots, account data, and personal trade context only in the private version or private RAG index.

When preparing a GitHub upload or public release, use only the public version and read `references/release-and-privacy.md` first. Run a privacy check for `Stocks/`, private RAG folders, `.ftindex`, `.env`, credentials, personal paths, raw source files, screenshots, and private labels.

## Workflow

1. Read `references/experience.md` before deep analysis, but only `Active Playbook` and `Compression Protocol` unless the user explicitly asks for history.
2. Read `references/sentiment-framework.md` when the task needs emotion-cycle classification, main-line judgment, crowded-trade risk, forum psychology, or cross-market sentiment. Read `references/release-and-privacy.md` before publishing, syncing public/private versions, or preparing a GitHub upload.
3. Gather or receive evidence from the market-specific skill first:
   - A-shares: prefer `cn-stock-move-reason` for quote, announcements, 股吧, board ranks, breadth, and A-share emotion cycle.
   - Japanese stocks: prefer `jp-stock-move-reason` for quote, news, Yahoo 掲示板, metrics, and theme/peer context.
   - US stocks/indexes: choose `us-stock-gamma-moomoo` for option/gamma questions and `stock-technical-analysis` for chart/trend questions; use both when positioning and price action both matter.
4. Classify the move through three lenses: `confirmed catalyst`, `emotion/positioning`, and `technical confirmation`. Do not let forum heat replace confirmed news.
5. If a multi-turn correction reveals a reusable lesson, update `references/experience.md` after answering. Generalize the lesson; remove ticker-specific personal details and private labels.

## Optional Private RAG

If the user wants to use private study materials, ask them to specify a local RAG or index folder. Do not assume a default private path. Use it only for extracting reusable rules relevant to the current task.

Rules for private RAG:

- Never copy raw private files, full passages, screenshots, API keys, account data, or personal trade logs into this public skill.
- Never write private folder paths into public files.
- Strip proprietary strategy names, private person names/handles, and memorable private labels.
- Summarize only public-safe, reusable principles into `references/experience.md` or `references/sentiment-framework.md` when the user explicitly asks to update the skill.
- Keep private indexes outside the Git repository. A user may maintain their own local index such as `private-rag/` or any folder they choose; it must be ignored by Git.
- When useful, offer to build or update a local index for the user's private RAG. The index should contain only file names or user-approved aliases, topics, page/slide ranges, keywords, and short public-safe summaries. It should not copy raw source text or include secrets.

### Local RAG Index Pattern

If the user asks to use private study materials repeatedly, propose a lightweight index stored outside the public repository. The same private RAG can support sentiment, technical analysis, gamma/option analysis, and cross-market study materials:

```text
private-rag-index/
  market-sentiment-framework.md
  technical-patterns.md
  gamma-notes.md
  macro-and-cross-market.md
```

Each index entry should be compact:

```text
- Topic: high-level divergence
  Source: user-private-file alias + page/slide range
  Keywords: climax, failed breakout, volume without progress
  Reusable rule: Late-cycle divergence after one-sided euphoria is riskier than early-cycle turnover.
  Public-safe: yes/no
```

Use the index to find relevant private material efficiently, then answer from public-safe distilled rules.

## Output Style

When used directly, answer in Chinese unless the user asks otherwise. Use this compact structure when useful:

1. `情绪结论`: risk-on/risk-off, early-cycle/late-cycle, panic, rotation, or crowded long.
2. `证据`: confirmed news, forum/post heat, breadth, sector peers, option/gamma positioning, and chart behavior.
3. `周期位置`: A-share seven-stage cycle when relevant; otherwise describe low-vol accumulation, early breakout, acceleration, distribution, or de-risking.
4. `主线判断`: leader/follower/defensive alternative/old-leader rebound/noise.
5. `验证条件`: what confirms continuation.
6. `失效条件`: what shows emotion has turned.

Do not give direct trading instructions. Give conditional conclusions and clearly label uncertain forum narratives as `思惑` or `未确认`.
