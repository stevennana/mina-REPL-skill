# REPL Source Traceability

This file explains how to interpret the guidance in `mina-repl-core`.

## Traceability Levels

Each major design statement in this skill should be understood as one of:

- **Verified**
  - directly supported by the inspected Codex or OpenCode source/docs
- **Inferred**
  - strongly implied by implementation shape or adjacent docs, but not stated directly in one place
- **Recommended**
  - a design choice made by this skill after comparing the upstream systems

## Traceability Rule

The more central a claim is to shell behavior, the closer it should be to `Verified`.

Examples:

- AGENTS/project-doc layering in Codex: `Verified`
- explicit plan/build distinction in OpenCode: `Verified`
- using those ideas to shape a Python REPL shell on `prompt_toolkit` and `rich`: `Recommended`

## Audit Focus Areas

The highest-value subsystems audited so far are:

- prompt and instruction layering
- context/history and compaction
- memories
- session lifecycle
- approval and permission handling
- tool registry and tool-loop state
- terminal UI patterns

Use the subsystem maps for the concrete upstream files behind those topics.
