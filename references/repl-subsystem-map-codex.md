# Codex Subsystem Map

This file maps the most relevant `openai/codex` subsystems to `mina-repl-core` guidance.

## Prompt And Instruction Layering

- `codex-rs/core/prompt.md`
- `codex-rs/protocol/src/prompts/base_instructions/default.md`
- `docs/agents_md.md`

Use these for:

- instruction precedence
- base vs developer instructions
- AGENTS/project-doc layering
- planning and responsiveness expectations

## Context And History

- `codex-rs/core/src/context_manager/history.rs`
- `docs/tui-chat-composer.md`
- `codex-rs/core/src/compact.rs`

Use these for:

- prompt-visible history
- local vs persistent draft/history state
- compaction behavior
- context-window pressure handling

## Memory System

- `codex-rs/core/src/memories/mod.rs`
- `codex-rs/core/src/memories/prompts.rs`
- `codex-rs/core/templates/memories/consolidation.md`

Use these for:

- progressive-disclosure memory design
- memory-tool developer instructions
- rollout-summary consolidation patterns

## Thread / Turn / Protocol

- `codex-rs/docs/codex_mcp_interface.md`
- `codex-rs/app-server-protocol/src/protocol/v2.rs`
- `sdk/typescript/src/items.ts`

Use these for:

- thread/turn lifecycle
- approval requests
- reasoning and todo-list items
- structured event/state concepts

## Tool And Config Layer

- `codex-rs/mcp-server/src/codex_tool_config.rs`
- `docs/config.md`

Use these for:

- schema-driven tool/session config
- explicit prompt overrides
- approval policy config
- state DB and plan-mode config behavior
