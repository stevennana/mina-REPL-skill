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
- `codex-rs/core/templates/agents/orchestrator.md`
- `codex-rs/app-server-protocol/schema/typescript/v2/Config.ts`
- `codex-rs/core/src/compact.rs`
- `codex-rs/core/src/memories/mod.rs`
- base-instructions templates
- memory-consolidation templates
- MCP codex tool configuration
- tools orchestrator and orchestrator templates
- Codex tracing / verbose logging docs
- `docs/js_repl.md` bounded vs trace logging

## OpenCode design-pattern baseline

- `anomalyco/opencode` `README.md`
- `anomalyco/opencode` `SECURITY.md`
- `anomalyco/opencode` `CONTRIBUTING.md`
- `anomalyco/opencode` `specs/project.md`
- `anomalyco/opencode` session prompt contracts
- `anomalyco/opencode` `read`, `grep`, and `task` tool docs
- `anomalyco/opencode` `glob` tool doc
- `anomalyco/opencode` project `config.mdx`
- `anomalyco/opencode` built-in `tools.mdx`
- `anomalyco/opencode` `provider/transform.ts`
- `anomalyco/opencode` `session/compaction.ts`
- `anomalyco/opencode` SDK OpenAPI session and permission schema
- `anomalyco/opencode` verification expectations from `CONTRIBUTING.md`
- `anomalyco/opencode` tool docs and registry files
- `anomalyco/opencode` plan/build prompt contracts
- `anomalyco/opencode` session system
- `anomalyco/opencode` session processor and LLM loop
- `anomalyco/opencode` debugging guidance from `CONTRIBUTING.md`

These are useful for extracting TUI-first, multi-client, session-centric terminal-agent patterns.

## Important note

The upstream `codex-cli/README.md` is legacy TypeScript documentation.
It is still useful for terminal-agent framing, but it should not be treated as the current
implementation architecture source of truth.
