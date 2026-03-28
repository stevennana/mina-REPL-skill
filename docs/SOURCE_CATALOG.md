# Source Catalog

The canonical machine-readable source catalog lives in `sources.yaml`.
The canonical deep explanation of source usage lives in `references/repl-source-baseline.md`.

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

## OpenCode design-pattern baseline

- `anomalyco/opencode` `README.md`
- `anomalyco/opencode` `SECURITY.md`
- `anomalyco/opencode` `CONTRIBUTING.md`

These are useful for extracting TUI-first, multi-client, session-centric terminal-agent patterns.

## Important note

The upstream `codex-cli/README.md` is legacy TypeScript documentation.
It is still useful for terminal-agent framing, but it should not be treated as the current
implementation architecture source of truth.
