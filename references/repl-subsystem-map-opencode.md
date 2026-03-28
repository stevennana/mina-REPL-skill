# OpenCode Subsystem Map

This file maps the most relevant `anomalyco/opencode` subsystems to `mina-repl-core` guidance.

## Session Lifecycle

- `packages/opencode/src/session/index.ts`
- `specs/project.md`

Use these for:

- session identity
- fork/compact/share/revert lifecycle
- project/worktree-aware session boundaries

## Prompt Contracts

- `packages/opencode/src/session/prompt/default.txt`
- `packages/opencode/src/session/prompt/codex.txt`
- `packages/opencode/src/session/prompt/plan.txt`
- `packages/opencode/src/session/prompt/build-switch.txt`
- `packages/opencode/src/session/prompt.ts`

Use these for:

- prompt-contract layering
- plan/build transitions
- prompt part resolution
- shell/operator style rules

## Permission System

- `packages/opencode/src/permission/index.ts`
- `packages/opencode/src/permission/evaluate.ts`
- `packages/opencode/src/permission/schema.ts`
- `SECURITY.md`

Use these for:

- permission request lifecycle
- allow/deny/ask rulesets
- UX approvals vs sandbox boundaries

## Tool Registry And Execution

- `packages/opencode/src/tool/registry.ts`
- `packages/opencode/src/tool/schema.ts`
- `packages/opencode/src/tool/tool.ts`
- `packages/opencode/src/tool/plan.ts`
- `packages/opencode/src/tool/todo.ts`

Use these for:

- discoverable tool ids and schemas
- prompt/tool boundary choices
- plan and todo tool behavior

## Agent / Model Layer

- `packages/opencode/src/agent/agent.ts`
- `packages/opencode/src/provider/models.ts`
- `packages/sdk/openapi.json`

Use these for:

- agent roles and default permissions
- provider/model selection
- session prompt request shapes
- visible session/tool/permission state in APIs
