# Source Catalog

The canonical machine-readable source catalog lives in `sources.yaml`.
The canonical deep explanation of source usage lives in `references/repl-source-baseline.md`.
The audit/traceability layer lives in `references/repl-source-traceability.md`.

This file is the short human-readable summary.

## Python implementation baseline

- Python `cmd`
- Python `code`
- Python `readline`
- Python `asyncio`
- `prompt_toolkit`
- `cmd2`
- `rich`
- `textual`
- `asyncssh`
- `ptpython`

## Codex design-pattern baseline

- root `openai/codex` `README.md`
- root `openai/codex` `AGENTS.md`
- `.codex/skills/*/SKILL.md`
- `codex-rs/skills` sample skill assets
- `codex-rs/tui_app_server/styles.md`
- `docs/tui-chat-composer.md`
- `codex-rs/docs/codex_mcp_interface.md`
- `docs/config.md`
- `codex-rs/core/prompt.md`
- base-instructions templates
- memory-consolidation templates
- MCP codex tool configuration

## OpenCode design-pattern baseline

- `anomalyco/opencode` `README.md`
- `anomalyco/opencode` `SECURITY.md`
- `anomalyco/opencode` `CONTRIBUTING.md`
- `anomalyco/opencode` `specs/project.md`
- `anomalyco/opencode` session prompt contracts
- `anomalyco/opencode` SDK OpenAPI session and permission schema
- `anomalyco/opencode` verification expectations from `CONTRIBUTING.md`
- `anomalyco/opencode` plan/build prompt contracts
- `anomalyco/opencode` session system

These are useful for extracting TUI-first, multi-client, session-centric terminal-agent patterns.

## Important note

The upstream `codex-cli/README.md` is legacy TypeScript documentation.
It is still useful for terminal-agent framing, but it should not be treated as the current
implementation architecture source of truth.
