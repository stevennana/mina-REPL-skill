# REPL Prompt Composition

This file describes how to compose prompt messages for a coding-agent shell on top of
`mina-repl-core`.

## Evidence Status

- **Verified:** Codex exposes base/developer/compact instruction concepts; OpenCode exposes explicit default/plan/build prompt contracts.
- **Inferred:** prompt composition works best as explicit layered templates rather than hidden string assembly.
- **Recommended:** `mina-repl-core` should preserve those layers as first-class shell concepts.

## 1. Use explicit instruction layers

Codex exposes `base_instructions`, `developer_instructions`, and `compact_prompt`.
OpenCode uses explicit prompt contracts for default, plan, and build behavior.

Recommended prompt composition order:

1. base/system instructions
2. developer/runtime instructions
3. scoped project-doc instructions
4. operational mode instructions (`plan` vs `build`)
5. current session memory summary
6. current plan/todo/review/tool state
7. user turn content

## 2. Do not overload one message with every responsibility

Split responsibilities cleanly:

- system/base: stable identity and safety posture
- developer/runtime: operational rules for this shell
- project docs: repo-scoped constraints and conventions
- turn payload: what the user wants now

This makes the prompt easier to reason about and easier to compact.

## 3. Mode switching should change instructions explicitly

OpenCode's plan/build prompt files and Codex collaboration modes both show that operational
behavior belongs in explicit prompt composition, not hidden internal flags alone.

Guidance:

- switching from `plan` to `build` should update the instruction layer explicitly
- the operator should understand that this happened
- the prompt should not silently retain obsolete read-only instructions during execution

## 4. Use compact prompts intentionally

Compaction should not merely "summarize the chat".

A good compact prompt should preserve:

- user intent
- relevant constraints
- current plan state
- key unresolved questions
- tool/review state that still matters

Do not compact away the information that explains what the shell is trying to do next.

## 5. Reasoning and todo state are context artifacts too

Codex exposes reasoning summaries and todo-list items as distinct thread items.

Guidance:

- treat plan/todo state as an explicit prompt input when it is relevant
- avoid forcing the model to reconstruct its own execution plan from raw transcript alone
- prefer compact, current plan state over replaying a long chain of earlier planning prose

## 6. Prompt composition should be model-aware

The active model configuration may change:

- reasoning effort
- personality/variant
- modality support
- provider behavior

Prompt composition should adapt explicitly to those model capabilities instead of assuming one
universal prompt shape for all providers and models.
