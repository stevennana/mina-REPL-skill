---
name: mina-repl-core
description: Foundational skill for building or extending a Python-native AI REPL runtime. Use when a project needs a multi-turn terminal interaction loop, explicit chat/shell/multiline modes, persistent history and transcripts, structured terminal rendering, or a REPL-first upgrade path to richer UI.
---

# Mina REPL Core

Use `mina-repl-core` when the project needs a reusable Python REPL substrate for an agent or
tooling shell. This skill is for the runtime layer, not for domain workflows.

Do not use this skill as the place to store product rules, approval policy, or business logic.
Those belong in higher-level project skills and repo-specific instructions.

## Read First

Before redesigning or extending a REPL, read these references:

- `references/repl-runtime-contract.md`
- `references/repl-architecture.md`
- `references/repl-extension-points.md`
- `references/repl-source-baseline.md`
- `references/repl-design-opencode.md`

## Use This Skill When

- the project needs a multi-turn prompt lifecycle
- chat, shell, and multiline modes need to stay explicit
- shell execution must remain separate from assistant text
- transcript and history persistence should be first-class
- a plain REPL should be able to grow into a richer terminal UI later

## Runtime Ownership

`mina-repl-core` should own:

- prompt lifecycle and mode switching
- slash-command dispatch
- transcript and history persistence
- shell execution through an explicit bridge
- structured rendering primitives

Higher-level project code should own:

- domain workflows
- business-specific tool routing
- approval and policy decisions
- repo or product conventions

## Workflow

1. Inspect the target repo or runtime first.
2. Decide whether the task is:
   - creating a new REPL runtime
   - extending the base runtime
   - refactoring a tangled runtime into clear boundaries
3. Keep the operator-visible contract explicit:
   - mode semantics
   - slash commands
   - shell boundaries
   - transcript and history behavior
4. Wire domain logic through the assistant callback or wrapper layer instead of embedding it in the runtime.
5. Add full-screen UI only after the basic REPL loop, shell bridge, and transcript contract are stable.

## Rules

- Keep one `asyncio` event loop for prompts, assistant calls, shell execution, and streaming work.
- Treat shell access as a tool channel with structured results, not as raw chat text.
- Preserve explicit `chat`, `shell`, and `multiline` modes.
- Persist both history and transcripts so the runtime is usable and reproducible.
- Keep input handling, execution, and rendering loosely coupled.
- Prefer `prompt_toolkit` + `rich` as the default Python stack unless the project already established a different runtime contract.

## Skill Assets

The canonical machine-readable payload for this skill lives at the repo root:

- `manifest.yaml`
- `contracts.yaml`
- `best_practices.yaml`
- `sources.yaml`
