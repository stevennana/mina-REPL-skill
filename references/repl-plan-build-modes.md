# REPL Plan And Build Modes

This file describes the recommended separation between read-only planning behavior and mutating
execution behavior in a richer agent shell.

## Separate Three Things

Do not collapse these layers together:

1. runtime input modes
   - `chat`
   - `shell`
   - `multiline`
2. operational agent modes
   - `plan`
   - `build`
3. approval/autonomy modes
   - `suggest`
   - `auto_edit`
   - `full_auto`

Each layer answers a different question:

- runtime mode: how input is routed
- operational mode: whether the agent is analyzing or mutating
- approval mode: how much may happen without confirmation

## `plan` Behavior

Recommended expectations:

- read-only by default
- inspect, search, and analyze freely
- ask clarifying questions when needed
- avoid file mutation and side-effectful commands
- produce an implementation-ready plan before switching to build

## `build` Behavior

Recommended expectations:

- file edits are permitted according to approval policy
- shell commands are permitted according to approval policy
- verification is part of the workflow, not an afterthought
- the shell should make the mode switch visible

## Transition Rules

- moving from `plan` to `build` should be explicit
- the shell should not silently mutate while still presenting itself as planning
- if the shell returns from build to analysis, that state change should also be explicit

## Why This Matters

This separation keeps agent shells understandable:

- planning stays safe and reviewable
- build behavior stays intentional
- approval/autonomy semantics remain clear
- runtime routing logic does not have to carry hidden behavioral policy
