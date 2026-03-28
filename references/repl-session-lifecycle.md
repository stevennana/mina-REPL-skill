# REPL Session Lifecycle

This file describes the session-level behavior that becomes important once a base REPL grows
into a more capable agent shell.

## Evidence Status

- **Verified:** OpenCode models session metadata, fork, compact, revert, and permission state as first-class concepts.
- **Inferred:** similar session concepts are necessary once a Python REPL shell grows beyond a minimal loop.
- **Recommended:** `mina-repl-core` should keep session lifecycle explicit instead of encoding it only in UI state.

## Why Session Lifecycle Matters

A useful coding-agent shell eventually needs more than a prompt loop.
It needs durable state around:

- session creation and resume
- transcript/history persistence
- branch or workspace review state
- fork/replay behavior
- summarization or compaction for long sessions

## Recommended Session Concepts

### Create / Resume

- a new session starts with a clean runtime state
- an existing session can be resumed with transcript/history context
- the shell should keep session identity separate from the transient prompt widget

### Fork

- forking creates a new session derived from an earlier point
- useful for alternative solution paths or partial replay
- should preserve enough context to explain lineage without mutating the original session

### Compact / Summarize

- long-running sessions benefit from explicit compaction
- compaction should be visible to the operator, not an invisible mutation of history
- preserve a summary artifact or session metadata rather than pretending no compaction occurred

### Review Surface

After file-changing actions, a stronger shell should make review state explicit:

- changed files
- diff availability
- whether VCS is present
- whether snapshot/review data is available

## Session Metadata

Once the shell grows beyond a minimal loop, recommended session metadata includes:

- session identifier
- title or summary
- parent session identifier for forks
- archived state
- last compaction time
- approval mode or permission state when relevant

## Layering Rule

The base runtime does not need to implement all of this immediately.
But a useful agent shell built on the runtime should model these concepts explicitly instead of
encoding them only in UI state or ad hoc files.
