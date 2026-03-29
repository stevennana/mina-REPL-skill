# REPL Approval And Autonomy

This file defines the recommended approval model for agent shells built on top of
`mina-repl-core`.

## Evidence Status

- **Verified:** Codex documents explicit approval modes and config overrides; OpenCode documents permissions and their non-sandbox nature.
- **Inferred:** approval/autonomy state belongs in the shell’s visible operator surface.
- **Recommended:** `mina-repl-core` should keep approval policy outside the prompt loop, route it through the orchestrator, and describe it honestly.

## Core Distinction

Approval policy is not the same thing as sandboxing.

- approvals are an operator UX and policy layer
- sandboxing is an execution-isolation layer

The runtime should document which one it actually provides.

## Recommended Approval Modes

### `suggest`

- reads may happen without confirmation
- file writes require confirmation
- shell commands require confirmation
- safest default for unfamiliar repos

### `auto_edit`

- reads and file edits may happen without confirmation
- shell commands still require confirmation
- useful when the operator trusts the model to patch code but not execute arbitrary commands

### `full_auto`

- reads, writes, and shell commands may proceed without per-action confirmation
- only appropriate when combined with a clearly documented environment policy
- should be coupled with explicit warnings for risky environments

## Safety Expectations

If a shell exposes higher-autonomy modes, it should make the environment contract explicit:

- whether network access is allowed
- whether writes are limited to the workspace
- whether the current directory is tracked by version control
- whether the shell is actually sandboxed or only approval-gated

Approval prompts should appear when the orchestrator selects a tool or shell action that crosses policy. They should not require the user to manually enter a separate shell mode first.

## Where Approval Logic Belongs

Keep approval logic outside the prompt loop.
Prefer one of these boundaries:

- shell bridge wrapper
- orchestration layer above the runtime
- session-level policy layer

Do not bury approval rules inside:

- rendering code
- prompt labels
- transcript serialization

## Operator Surface

If approval modes exist, the shell should make the current mode visible and queryable.

Minimum expectations:

- the current approval mode is discoverable in status output
- the user can tell whether the shell is read-only, edit-capable, or fully autonomous
- the user is warned when high-autonomy modes run outside a safe or versioned workspace

## Recommended Default

For a new coding-agent shell:

- default to `suggest`
- add `auto_edit` and `full_auto` only when their behavior is precisely documented
- keep the documentation honest when approvals are UX rather than hard security
