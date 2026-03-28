# REPL Tool Loop And Turn Orchestration

This file describes the recommended multiturn orchestration model for an agent shell built on top
of `mina-repl-core`.

## 1. Think in threads and turns

Codex models conversations as threads and turns.

Guidance:

- treat the session as the durable conversation container
- treat each user request as a turn
- allow a turn to span multiple model/tool/approval steps before completion

## 2. Keep the tool loop explicit

A useful turn often follows this pattern:

1. user turn starts
2. model reasons and decides on a tool
3. shell checks whether approval is needed
4. tool executes
5. tool result is returned to the model
6. model either calls more tools or produces a response

This should be visible as a state machine, not a hidden recursive loop.

## 3. Tool registry and schema should be discoverable

OpenCode exposes tool IDs and tool schemas; Codex exposes approval and tool-session interfaces.

Guidance:

- make available tools inspectable
- keep tool parameters explicit
- do not make tool choice rely on hidden Python-only knowledge

## 4. Expose turn state to the operator

At minimum, an advanced shell should be able to surface:

- current turn id
- active tool
- waiting for approval vs running tool vs waiting on model
- whether the turn is interruptible

This prevents the shell from feeling like a black box.

## 5. Interrupts and approvals belong in the loop

Turns should support:

- interrupting active work
- pausing for approval
- resuming after approval or tool result

These are part of the orchestration contract, not just UI details.

## 6. Tool calls should remain reviewable

When possible, keep tool activity reviewable through:

- structured tool results
- explicit state transitions
- bounded summaries in operator-facing output

Do not reduce all tool behavior to raw text dumps.
