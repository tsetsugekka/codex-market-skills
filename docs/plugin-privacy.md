# DayTradingMonster Market Analyst — Privacy notice

Effective: 2026-09-11. Scope: the skills-only plugin distributed from this repository.

## What the package does

The plugin bundles instructions, reference files and scripts for market research. It does not configure a publisher-hosted MCP server, a plugin account system or an analytics/telemetry service that receives every conversation. Installing this package does not give its maintainer access to a user's ChatGPT conversations or local files.

## Data used during a workflow

The host (such as ChatGPT or Codex) processes prompts, attachments and any files the user allows it to access under the host's own terms and privacy controls. A workflow may read user-supplied price tables, option chains or research material, and may save requested reports or local working files in the user's environment. Their retention depends on the host and the user's storage settings.

The host's browsing/data tools and the bundled scripts may contact market-data and news services, including DayTrading.monster, or locally installed data providers. Those services may receive requested symbols, query parameters and normal connection information. Requests and any provider-side logging are subject to the respective provider's terms and privacy practices. This notice does not promise zero logging or a fixed retention period for third-party services.

Optional Google Calendar actions use a separately authorized connection and may send event details when the user requests calendar creation or updates. OpenD and MX dependencies run only where separately available and authorized. The package does not require credentials to be posted in a chat or public issue.

## Support and control

Support is provided through [GitHub Issues](https://github.com/tsetsugekka/codex-market-skills/issues). Issues are public: include a sanitized problem description only, never API keys, cookies, account identifiers, positions or private documents. GitHub processes issue content under its own policies. For an issue you submitted, edit or remove it using GitHub controls, or ask the maintainer to remove sensitive content without repeating that content.

Disable or uninstall the plugin to stop using its workflows. Manage host conversation/file retention and revoke connected-service access in the respective products. Uninstalling the package does not delete records held by those products or data providers.

Material changes to this package's data-handling behavior will be reflected in this notice alongside the relevant release.
