---
name: cn-stock-move-reason
description: Use when analyzing why one A-share stock moved sharply using Codex, without Gemini, from Eastmoney quote data, announcements, Eastmoney 股吧/资讯 posts, Sohu index/sector context, and A-share breadth.
metadata:
  short-description: Analyze A-share move reasons from announcements, 股吧, index/sector context, and emotion cycle
---

# CN Stock Move Reason

Use this skill when the user asks why one A-share stock is rising, falling, 涨停, 跌停, 炸板, 异动, or moving unusually, and wants Codex to analyze it instead of Gemini.

The bundled script is safe for a public repository: it uses only public web pages/APIs, does not read credentials, and does not call any LLM service.

The skill accepts one stock at a time. It may also collect broad market context (indexes, sector/concept boards, and advance/decline counts) to judge whether the move is market-wide, sector-led, or stock-specific.

## Workflow

1. Read `EXPERIENCE.md` before analysis, but only the `Active Playbook` and `Compression Protocol` sections unless the user explicitly asks for historical lessons. Apply those lessons when judging catalysts, sector共振, 股吧 emotion, and A-share emotion-cycle position.

2. Run the collector script from the repository root:

```bash
python3 skills/cn-stock-move-reason/scripts/stock_move_sources.py 600519 --format markdown
```

Useful options:

- `--hours 24`: evidence window.
- `--posts 100`: maximum Eastmoney 股吧/资讯 rows to include. The default is 100.
- `--announcements 10`: maximum announcements to include.
- `--skip-market-context`: skip indexes, sector/concept boards, and advance/decline counts when the user wants only single-stock materials.

3. If network access fails in Codex, rerun the same command with sandbox escalation according to the normal approval policy.

4. Analyze the script output directly. Do not call Gemini. Treat sources with this priority:

- Announcements, earnings, regulatory filings, and confirmed company materials: primary evidence.
- Eastmoney 股吧资讯/high-read posts: secondary evidence; useful for discovering what the market is discussing.
- Sohu index and sector/concept board context plus Eastmoney intraday advance-decline counts and Sohu historical advance-decline / limit-up / limit-down data: market/sector backdrop only; use it to judge 共振 versus 独立催化.
- Ordinary 股吧 posts: emotion and speculation only. Never treat them as confirmed fact unless the same item appears in announcements/news.

5. In multi-turn discussions about the same stock, treat user follow-ups as possible new evidence or feedback. If the user adds information, challenges the reasoning, asks for reconsideration, or the conversation reveals that the prior answer missed/misweighted something, re-evaluate the stock with the new context before defending the earlier answer.

6. If the analysis or multi-turn correction produces a durable new lesson, update `EXPERIENCE.md` after answering. Follow its `Conversation Learning Protocol` and `Compression Protocol`: generalize the lesson, merge repeated lessons into the active summary, keep the active section short, and move only distinct older details into the archive.

## A-share Emotion Cycle

Classify the short-term emotion backdrop qualitatively into one of seven stages from the single-stock materials, price action, 股吧 discussion, market indexes, sector/concept boards, today's breadth, and recent Sohu zdt history:

1. `冰点期`: many limit-downs or large losers, high failed-board/亏钱效应, shrinking participation. Observe who resists the selloff.
2. `修复/潜伏期`: panic eases, limit-downs decrease, front-row names begin to rebound, but most traders are still skeptical. Small trial positions only.
3. `启动期`: new theme appears, first/second boards increase, capital starts focusing. Prefer front-row names in the core theme.
4. `加速期`: leaders continue limit-up, followers spread, sector赚钱效应 is strong. Hold strength, avoid random laggards.
5. `高潮期`: everyone discusses the theme, limit-up wave or one-word boards, retail emotion is hot. Take profits progressively; do not chase heavily.
6. `高位分歧/分化期`: after高潮, leaders may炸板/断板/long upper shadow while back-row names weaken, but the whole market has not fully collapsed yet. Treat it as the transition from emotion top to退潮.
7. `退潮期`: leaders break down, 天地板/核按钮 rise,亏钱效应 spreads. Reduce exposure or wait.

Useful loop: `冰点 -> 修复/潜伏 -> 启动 -> 加速 -> 高潮 -> 高位分歧/分化 -> 退潮 -> 再冰点`.

`分歧` is not always bearish. A healthy divergence during 启动/加速 can be a换手 test or main-line pullback before renewed agreement; a high-level divergence after高潮 is usually a risk signal. The favorable windows are usually late 修复 to early 启动, and healthy main-line divergence before 加速. The most dangerous windows are late 高潮, 高位分歧/分化, and early 退潮.

## Reading News And Emotion

- Separate `confirmed catalyst` from `market imagination`. A confirmed order, policy, earnings beat, regulatory approval, or buyback is stronger than a forum narrative.
- Decide whether the stock is an `情绪票` or a `趋势票`:
  - 情绪票: topic-driven, high volatility, limit-up relay, fast climax/retreat.
  - 趋势票: supported by industry cycle, earnings, policy, or institutional logic; slower but more durable.
- Watch for emotional-top clues: high attention, continuous large candles, high turnover, failed breakout, long upper shadow, break-board/炸板, or broad follower exhaustion.
- Watch for trend-risk clues: good news priced in, valuation stretch, volume-price divergence, loss of key moving averages, or gradual weakening after a crowded story.

## Output Style

Reply in Chinese unless the user asks otherwise. The answer can be detailed because this is a single-stock local script workflow. Use this order:

1. `最有力理由`: most likely catalyst, with source names and timing.
2. `补助理由`: secondary drivers such as theme, sector rotation, liquidity, valuation, or positioning.
3. `共振判断`: whether the stock is moving with the market, its sector/concept, or mostly on stock-specific news.
4. `情绪面/周期位置`: qualitative 股吧 emotion plus the seven-stage A-share emotion cycle.
5. `确定度`: high / medium / low, with one sentence explaining why.
6. `注意点`: what remains unconfirmed or what could invalidate the read.

If evidence is weak, say so plainly and use wording like `思惑`, `低信息量`, `未确认`, or `确认待ち`. Do not invent catalysts absent from the collected evidence.
