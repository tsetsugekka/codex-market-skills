# DayTrading.Monster — compatibility and release status

The display name is **DayTrading.Monster** and the stable package identifier is `codex-market-skills`. This repository maintains two delivery variants of the same research suite.

| Variant | Authoritative source | Installation |
| --- | --- | --- |
| Standalone Codex workflows | Root `skills/` and root `.codex-plugin/` | Individual skills or the repository marketplace entry |
| Environment-aware marketplace plugin | `plugin/skills/` and `plugin/.codex-plugin/` | DayTrading.Monster in the plugin store |

The variants may differ in runtime instructions. The marketplace build includes the full shared research references listed in `plugin/shared-references.json` and portable Python in `plugin/shared-scripts.json`, plus the offline forum entry point. It does not bundle external data-provider skills or require a user's local machine. Avoid installing duplicate same-name skills unless comparing variants deliberately.

## Capability routing

ChatGPT Web, ChatGPT work environments and Codex can expose different tools. Discover actual tools, connectors, skills and execution capabilities for each session; do not decide availability from the product name. A connector can provide a useful capability without a same-name Skill.

- Reuse supplied evidence and accessible public sources first; query only missing material.
- Use authorized OpenD/moomoo, MX, Hithink or equivalent tools when available. A cloud workspace is not automatically connected to a user's local OpenD.
- Full-chain Gamma, Vanna, scenario tables and charts require suitable inputs and actual computation. The marketplace variant retains the methods and can use any available execution environment; the fixed DTM SPX feed alone cannot produce arbitrary-ticker full chains.
- Calendar planning is available without calendar write access. Writes require the user's request, an authorized connection, duplicate checks and readback.
- Six bundled scripts use Python 3.10+ and the standard library. Forum filtering and option scenario tables work offline with supplied inputs; quote/ranking/calendar/news collection also needs network access. Package upload, file access, Python execution and network access are separate acceptance checks. See the [runtime contract](../plugin/skills/market-daily-strategist/references/runtime-capabilities.md).
- Scheduled Tasks loading is not established by successful use in an ordinary chat or Codex. Keep the task's output, archive and authorization contracts.

## Release status

As of 2026-09-25 (Japan time):

- Source version 0.1.11 updates strategy and technical analysis to the index-trajectory `/api/range/nikkei` and `/api/range/sse` contracts. It has not been submitted to the marketplace; the published version remains 0.1.10.

- Marketplace 0.1.10 is published. The developer portal shows Published and the public plugin directory displays version 0.1.10; it replaces 0.1.9.
- Version 0.1.10 restores the full ten entries, source order/links, market report profiles and detailed research references. Its 47-file archive includes six Python scripts and shared live/offline forum filtering. Ten automated tests, ten Skill validators and the plugin manifest validator passed locally. The platform accepted the Python attachments, passed all ten Skill scans, approved the submission and published it after the maintainer confirmed the four required declarations.
- Live execution in ChatGPT Web/Work and loading by Scheduled Tasks remain unverified. Successful Python attachment ingestion does not establish execution or network access in those hosts; use the capabilities actually exposed in each session.
- The root manifest remains the standalone Codex variant at 0.1.6. Its version does not describe the separate marketplace package.
- Existing installations update through their host; source synchronization does not replace local caches.

See [plugin maintenance](../plugin/docs/MAINTENANCE.md) for package boundaries, build commands and the method coverage matrix, and [review scenarios](plugin-submission-tests.md) for expected behavior. Static validation, platform scanning, marketplace publication and live runtime acceptance are separate checks.
