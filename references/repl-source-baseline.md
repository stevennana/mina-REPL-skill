# REPL Source Baseline

This skill draws from two source families:

- Python-native REPL references for implementation details
- current `openai/codex` repository materials for skill packaging and terminal-agent design patterns

## Python-Native References

Use these as the implementation baseline:

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

These sources define the Python REPL mechanics, event loop model, completion patterns, transcript
testing patterns, and rendering primitives.

## Codex References

Use these as design-pattern references:

- root `openai/codex` `README.md` for the current product framing
- root `openai/codex` `AGENTS.md` for instruction layering and repo guidance
- `.codex/skills/*/SKILL.md` for concise skill structure
- `codex-rs/skills` sample skills for `references/`, `agents/`, and script-aware skill packaging

## Important Note About `codex-cli/README.md`

The `codex-cli/README.md` in the upstream repo is explicitly marked as legacy TypeScript
documentation. It is still useful for historical terminal-agent ideas such as:

- REPL framing
- permission and approval vocabulary
- memory and project-doc layering
- history as a first-class concern

But it should not be treated as the current implementation architecture source of truth.

## Extraction Rules

- Prefer current root docs and current skill samples when upstream sources disagree.
- Prefer Python-native docs for runtime behavior details.
- Use Codex sources mainly for packaging, instruction layering, and terminal-agent design posture.
- For exact upstream coverage, use `repl-source-traceability.md`, `repl-subsystem-map-codex.md`, and `repl-subsystem-map-opencode.md`.
