# REPL Tool Selection And Usage

This file captures practical tool-selection and tool-usage guidance extracted from Codex and
OpenCode.

## Evidence Status

- **Verified:** OpenCode explicitly instructs the agent to prefer specialized file tools over shell, to use `Glob` and `Grep` for search, and to use `Task` only for broader multi-step exploration.
- **Verified:** Codex has explicit tool registry, routing, and typed tool-output layers, plus approval/sandbox-aware orchestration.
- **Inferred:** efficient shell behavior depends on selecting the cheapest tool that answers the question before escalating to more general tools.
- **Recommended:** `mina-repl-core` should publish concrete tool-selection guidance instead of leaving tool choice entirely to intuition.

## 1. Prefer specialized tools over generic shell commands

Use the narrowest tool that answers the question:

- file content lookup: `read`
- filename discovery: `glob`
- content search across files: `grep`
- open-ended multi-step exploration: `task`
- raw shell commands: only when a specialized tool is not enough or when execution is itself the task

When the question is about the current workspace, first reuse any workspace context the shell
already knows before running new discovery commands.

## 2. Use `glob` and `grep` before broad file reads

For codebase exploration:

- use `glob` to narrow candidate files by path or suffix
- use `grep` to find matching content
- only then `read` the most relevant files

This keeps tool usage fast and keeps context smaller.

For workspace discovery, this same rule means:

- inspect cheap directory or metadata context first
- then narrow with `glob`, `grep`, and `read`
- only then escalate to broader shell execution

## 3. Avoid tiny repeated reads

When reading files:

- prefer larger windows over many tiny slices
- use line offsets intentionally
- avoid “30 lines at a time” churn unless a file is truly huge and the target area is still unknown

## 4. Parallelize independent reads and searches

When two tool calls do not depend on each other:

- run them in parallel
- batch related searches together

This is especially useful for:

- `git status` + `git diff`
- reading two or three known relevant files
- globbing and grepping multiple likely code locations

## 5. Keep the `task` tool for open-ended work

OpenCode is explicit that `Task` is not the first answer to every search problem.

Use `task` when:

- the work is multi-step or open-ended
- you need another agent/subagent to investigate autonomously
- the question is broader than a few files or one quick search

Do not use `task` when:

- you already know the file path
- you only need a direct grep/glob/read result
- the target is a very small known set of files

## 6. Make tool choice approval-aware

In a richer shell:

- reads and metadata lookups are usually cheaper and safer than writes or shell execution
- shell commands may cross approval boundaries
- tool selection should account for whether the operator is in suggest, auto-edit, or full-auto style modes

If the next safe read-only step is obvious, the shell should run it instead of replying with a
copy-paste command for the user.

## 7. Keep tool outputs reviewable

Tool outputs should remain structured enough to support:

- transcript recording
- review surfaces
- follow-up tool calls
- bounded summaries instead of raw dumps

## 8. Practical rule for file extraction

For file-oriented reasoning, the normal order should be:

1. `glob`
2. `grep`
3. `read`
4. `task` if the search remains open-ended
5. shell only if you need execution or a capability not covered by the specialized tools

For AI-oriented shells, prefer discovery by action over discovery by instruction.
