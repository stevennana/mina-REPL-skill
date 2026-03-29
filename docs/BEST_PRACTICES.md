# Best Practices

This repo now keeps the canonical skill-consumed guidance in `references/`.

Read these first for the actual REPL best-practice material:

- `references/repl-runtime-contract.md`
- `references/repl-context-engineering.md`
- `references/repl-prompt-composition.md`
- `references/repl-memory-and-model-config.md`
- `references/repl-prompt-templates.md`
- `references/repl-mcp-and-tool-registry.md`
- `references/repl-tool-selection-and-usage.md`
- `references/repl-tool-loop-and-turn-orchestration.md`
- `references/repl-plan-execution.md`
- `references/repl-approval-and-autonomy.md`
- `references/repl-session-lifecycle.md`
- `references/repl-plan-build-modes.md`
- `references/repl-terminal-ui-best-practices.md`
- `references/repl-verification-and-evaluation.md`
- `references/repl-failure-and-recovery.md`
- `references/repl-maturity-matrix.md`
- `references/repl-source-traceability.md`
- `references/repl-subsystem-map-codex.md`
- `references/repl-subsystem-map-opencode.md`
- `references/repl-source-baseline.md`

Use this `docs/` copy as a short contributor-facing summary only.

## Summary

- Keep the skill entrypoint concise and procedural.
- Keep REPL modes explicit.
- Treat shell execution as a separate tool channel.
- Persist both history and transcripts.
- Keep the runtime separate from product-specific policy and workflows.
- Prefer Python-native REPL references for implementation details and Codex sources for packaging and terminal-agent design posture.
