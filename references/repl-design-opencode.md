# OpenCode Design Notes

This file captures the REPL and terminal-agent design guidance extracted from
`https://github.com/anomalyco/opencode`.

Use it as a design-pattern reference, not as a Python implementation template.

## 1. Treat the TUI as one client, not the whole system

One of OpenCode's clearest architectural choices is that the TUI is not the whole application.
Its contributing docs split:

- core business logic and server
- TUI frontend
- shared app UI
- desktop wrapper
- headless server mode

Guidance for `mina-repl-core`:

- keep the Python REPL runtime usable as a standalone terminal loop
- avoid coupling core session logic to one presentation layer
- preserve the option to add web, desktop, or richer TUI shells later

## 2. Separate planning from execution

OpenCode exposes distinct agent behaviors:

- `build` for normal execution
- `plan` for read-only analysis

It also uses explicit prompt switching when moving from planning to execution.

Guidance for `mina-repl-core`:

- keep planning/execution distinctions explicit when a downstream project needs them
- do not overload a single mode with conflicting read-only and mutating responsibilities
- if planning is added, model it as an explicit session or agent behavior, not a hidden convention

## 3. Permissions are not the same thing as sandboxing

OpenCode's security docs are unusually explicit: permissions are a UX layer, not a security
boundary, and the product is not sandboxed by default.

Guidance for `mina-repl-core`:

- do not imply that prompt confirmations equal isolation
- document clearly whether a project's shell controls are approvals, policy checks, or real sandboxing
- if true isolation is required, treat it as infrastructure outside the base runtime

This is especially important for Python REPL projects that may be tempted to blur "ask before
running" with "safe to run".

## 4. Session state deserves first-class structure

OpenCode has a dedicated session layer, with support for:

- session creation and updates
- permission state on sessions
- message streams
- session diff and review state
- sharing and forking

Guidance for `mina-repl-core`:

- keep session state as an explicit concept rather than just an ad hoc prompt loop
- make transcript/history/session metadata durable and queryable
- preserve clear boundaries between prompt handling, message persistence, and review/export behavior

## 5. Keep operator controls visible

OpenCode surfaces many operator-facing controls around:

- agent selection
- session management
- permissions
- model/provider switching
- review panes and status dialogs

Guidance for `mina-repl-core`:

- preserve a visible control surface for session state and runtime mode
- make mode changes, shell actions, and review/export actions obvious in the interface
- do not hide critical runtime state behind implicit defaults only

## 6. Strong terminal posture still benefits from multiple surfaces

OpenCode is TUI-first, but not TUI-only.
It explicitly supports:

- terminal UI
- headless server mode
- web app
- desktop app

Guidance for `mina-repl-core`:

- design the Python REPL as a reusable terminal runtime adapter
- avoid hard-wiring assumptions that make reuse by a headless API or another client impossible
- keep shell, session, and transcript logic independent from terminal-specific rendering concerns

## 7. Development ergonomics matter for terminal products

OpenCode's contributing docs make the development modes explicit:

- local dev command behavior
- headless server mode
- separate frontend/backend workflows
- debugging paths

Guidance for `mina-repl-core`:

- document how to run the base runtime clearly
- keep demo and development workflows deterministic
- make the "plain REPL" path easy before adding richer wrappers

## 8. Practical synthesis for this skill

The useful OpenCode extraction for a Python REPL base is:

- TUI-first is compatible with multi-client architecture
- planning vs execution should be explicit
- permissions should be documented honestly as UX or policy, not marketed as sandboxing
- sessions should be first-class state, not incidental chat logs
- operator controls should remain visible and intentional

These principles fit well with the existing `mina-repl-core` emphasis on:

- explicit chat/shell/multiline modes
- shell as a dedicated tool channel
- transcript/history durability
- REPL-first architecture with a later upgrade path
