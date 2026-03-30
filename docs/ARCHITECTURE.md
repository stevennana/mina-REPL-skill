# Architecture

This repo is a hybrid skill root and Python package.

## Skill-facing layer

Canonical skill files live at the repo root:

- `SKILL.md`
- `manifest.yaml`
- `contracts.yaml`
- `best_practices.yaml`
- `sources.yaml`
- `agents/openai.yaml`
- `references/`

These are the files a symlinked Codex skill should rely on.

## Package-facing layer

The Python runtime lives under `src/mina_repl_core/`.

Key modules:

- `session.py` for prompt lifecycle and routing
- `shell.py` for command execution
- `transcript.py` for transcript persistence
- `manifest.py` for packaged asset loading

## Asset sync

The repo-root YAML files are canonical.
`tools/sync_skill_assets.py` mirrors them into `src/mina_repl_core/data/` for packaging.

## Canonical deep guidance

For detailed runtime architecture, read:

- `references/repl-runtime-contract.md`
- `references/repl-context-engineering.md`
- `references/repl-prompt-composition.md`
- `references/repl-memory-and-model-config.md`
- `references/repl-discovery-and-workspace-awareness.md`
- `references/repl-project-root-and-repo-scouting.md`
- `references/repl-prompt-templates.md`
- `references/repl-mcp-and-tool-registry.md`
- `references/repl-tool-selection-and-usage.md`
- `references/repl-tool-loop-and-turn-orchestration.md`
- `references/repl-orchestrator-guidance.md`
- `references/repl-plan-execution.md`
- `references/repl-approval-and-autonomy.md`
- `references/repl-session-lifecycle.md`
- `references/repl-plan-build-modes.md`
- `references/repl-architecture.md`
- `references/repl-extension-points.md`
- `references/repl-three-surface-ux.md`
- `references/repl-terminal-ui-best-practices.md`
- `references/repl-llm-logging-and-observability.md`
- `references/repl-verification-and-evaluation.md`
- `references/repl-failure-and-recovery.md`
- `references/repl-maturity-matrix.md`
- `references/repl-source-traceability.md`
- `references/repl-subsystem-map-codex.md`
- `references/repl-subsystem-map-opencode.md`
- `references/repl-source-baseline.md`
- `references/repl-design-opencode.md`
