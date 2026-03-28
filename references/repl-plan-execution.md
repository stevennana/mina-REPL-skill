# REPL Plan Execution

This file describes how a richer agent shell should manage plans, plan execution, and transitions
between planning and implementation.

## 1. Keep plan creation explicit

Planning is not just “thinking before typing”.
The shell should model planning as an explicit artifact or state.

Minimum expectations:

- there is a known plan/build distinction
- the operator can tell whether the shell is still planning
- planning can produce a structured plan, checklist, or step set

## 2. Plan mode should be read-only by default

OpenCode's plan prompt makes read-only behavior explicit before build mode begins.

Guidance:

- do not mutate files or run side-effectful commands while still in planning mode
- ask clarifying questions while planning when needed
- make the transition into build mode explicit

## 3. Plans should remain reviewable during execution

Good plan execution surfaces:

- current plan id or title
- current step
- completed steps
- blocked steps
- whether compaction changed the available context

This aligns with Codex's todo/plan visibility and with OpenCode's session-level state model.

## 4. Plan execution should integrate with session lifecycle

Plans should work with:

- session creation and resume
- session fork for alternate solution paths
- compaction/summarization
- review/diff state after mutations

Do not model plans as a one-shot prompt that disappears once execution starts.

## 5. Recovery paths matter

An execution-oriented shell should support recovery behavior such as:

- interrupt current work
- re-enter planning
- fork from an earlier point
- compact and continue
- review and potentially revert changed output

## 6. Practical rule

If the shell exposes plans, it should make them:

- visible
- reviewable
- resumable
- clearly separate from raw chat text
