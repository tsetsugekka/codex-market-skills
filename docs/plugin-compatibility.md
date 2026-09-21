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

As of 2026-09-21 (Japan time):

- Marketplace 0.1.9 is published. The developer portal shows Published and the public plugin directory displays version 0.1.9; it replaces 0.1.8.
- Marketplace source 0.1.10 further restores the full ten entries, source order/links, market report profiles and detailed research references. It adds portable Python and shared live/offline forum filtering. Local package and forum tests passed; platform scanning and publication of 0.1.10 are pending.
- The root manifest remains the standalone Codex variant at 0.1.6. Its version does not describe the separate marketplace package.
- Existing installations update through their host; source synchronization does not replace local caches.

See [plugin maintenance](../plugin/docs/MAINTENANCE.md) for package boundaries, build commands and the method coverage matrix, and [review scenarios](plugin-submission-tests.md) for expected behavior. Static validation, platform scanning, marketplace publication and live runtime acceptance are separate checks.
