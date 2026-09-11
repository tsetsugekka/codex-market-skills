# Plugin compatibility and release status

This repository contains one skills-only plugin with ten skills. `.codex-plugin/plugin.json` defines the package; `.agents/plugins/marketplace.json` makes the same package discoverable from the repository root. Neither file installs data providers.

## Runtime requirements

- Stock-move, macro, sentiment, technical and strategy workflows require fresh sources through the host's web/data tools. Optional third-party skills are not bundled.
- Full-chain gamma requires local moomoo OpenD, the moomoo Python SDK and the separate moomooapi skill at the location documented in the gamma skill. Cloud-only ChatGPT cannot reach a user's local OpenD by installing this bundle. The documented DTM SPX reference supports limited SPX context, not arbitrary-ticker full-chain computation.
- Some A-share theme workflows require MX skills and authorized data access. Missing providers must be reported; do not fabricate results.
- Calendar writes require an authorized Google Calendar connection and an explicit user request. Calendar planning alone does not prove calendar write access.
- Execute bundled scripts relative to their installed skill directory. Plugin caches do not use the standalone global-skill path.

## Validation and publication

2026-09-11: the compatibility manifest and all ten skill frontmatters passed the bundled validators; all thirteen Python scripts passed syntax parsing. These are static checks, not live data or ChatGPT installation acceptance tests.

Version 0.1.1 corrects gamma command paths and discloses its external helper dependency. Public directory submission and account installation are still pending. GitHub publication alone does not complete either step.

Public submission uses the [OpenAI plugin submission portal](https://platform.openai.com/plugins) and requires a selected name, verified developer identity, listing assets and policy URLs, five positive and three negative test cases, and platform review. See the [official submission requirements](https://developers.openai.com/plugins/deploy/submission).
