# REPL Maturity Matrix

This file helps distinguish what belongs in different shell maturity levels.

## Base Runtime

- prompt loop
- internal runtime routing states when needed
- shell bridge
- transcripts and history
- structured rendering

## Agent Shell

- approval modes
- plan/build behavior
- explicit memory policy
- tool loop state
- session lifecycle
- review surface

## Advanced Multi-Client Shell

- headless/server mode
- inspectable tool registry
- stronger model/config controls
- compaction policy
- richer verification and recovery playbooks

## Rule

Do not force a minimal REPL to implement the entire advanced shell contract.
Use the matrix to decide which layers are required now and which should remain optional.
