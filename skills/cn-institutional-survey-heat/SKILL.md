---
name: cn-institutional-survey-heat
description: Use when the user asks which A-share stocks, sectors, industries, or themes have the most institutional research visits / 机构调研 heat over the last 7 days, recent weeks, May-June, two months, or a custom date range. Produces stock Top 10, sector/industry Top 10, and weekly sector heat trends from Eastmoney institutional survey detail records.
metadata:
  short-description: A-share institutional survey heat and weekly sector trends
---

# CN Institutional Survey Heat

Use this skill for A-share institutional research / 机构调研 heat questions such as:

- `最近7天调研最多的股票`
- `最近7天机构调研最多的板块`
- `5-6月每周板块调研热度`
- `哪些行业机构调研在升温`
- `机构调研热度 Top 10`

This skill is a data-collection and aggregation helper. It does not give buy/sell instructions. Treat high institutional survey heat as attention and research intensity, not as a trading signal by itself.

## Default Workflow

Run the bundled script from the repository root:

```bash
python3 skills/cn-institutional-survey-heat/scripts/institutional_survey_heat.py
```

Default output:

1. `调研最多股票 Top 10`: last 7 natural days.
2. `板块/行业调研热度 Top 10`: last 7 natural days.
3. `Top 板块周度调研热度`: last 2 calendar months including the end date's month.

Useful options:

```bash
python3 skills/cn-institutional-survey-heat/scripts/institutional_survey_heat.py --end-date 2026-06-30
python3 skills/cn-institutional-survey-heat/scripts/institutional_survey_heat.py --days 7 --months 2 --top 10
python3 skills/cn-institutional-survey-heat/scripts/institutional_survey_heat.py --format json
python3 skills/cn-institutional-survey-heat/scripts/institutional_survey_heat.py --save-csv --output-dir /private/tmp/survey_heat
```

## Data And Rate Discipline

- Source table: Eastmoney institutional survey detail records, `RPT_ORG_SURVEYNEW`.
- Industry/sector labels come mechanically from the Eastmoney quote industry field `f100`; do not hand-classify sectors unless the user explicitly asks for a custom theme mapping.
- Count only institution rows: `RECEIVE_OBJECT_TYPE == 001`.
- For stock rankings, count unique institution names per stock within the window.
- For sector rankings, aggregate stock-level institution counts to the Eastmoney `f100` industry field, then sort industries by total count.
- `主要贡献股票` is generated mechanically: within each industry, sort stocks by institution count descending and display the top contributors.
- For weekly sector heat, count unique institution names per stock-week, then aggregate stock-week counts to the Eastmoney `f100` industry field.
- Default cache directory is under the system temp directory. Repeated same-window requests reuse cached raw rows and industry lookups unless `--no-cache` is set.
- Keep requests low frequency. The script paginates survey records with a short delay and batches industry lookups; do not loop it repeatedly.

## Interpretation

- `机构数` means unique institutional research participants under the script's de-duplication rule, not the number of separate meetings.
- `行业` and `主要贡献股票` are data-driven outputs from the script, not model-written summaries. The model may interpret the result afterward, but should not silently relabel industries or contribution stocks.
- Sector heat is an activity measure. The same institution can count once for each stock it researched in the same sector, because the goal is sector-level research intensity.
- Date windows use `RECEIVE_START_DATE`, not announcement date.
- Partial weeks can appear at the start/end of a custom window. Call this out when interpreting weekly trends.
- Use `cn-stock-move-reason`, `stock-sentiment-analysis`, or `stock-technical-analysis` only after a user asks for why a specific stock/sector is hot, whether it is tradable, or whether price confirms the research heat.

## Output Guidance

When answering, include:

1. Date window and counting method.
2. Stock Top 10 with code, name, institution count, industry, and survey dates.
3. Industry Top 10 with total heat and leading stocks.
4. Weekly industry heat table for the Top sectors.
5. A short read of rising/falling heat, while avoiding direct trading instructions.
