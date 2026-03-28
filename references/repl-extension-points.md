# REPL Extension Points

This file describes the supported ways to adapt `mina-repl-core` without turning it into an
application-specific monolith.

## Assistant Callback

The main extension point is the assistant callback:

- accept user text plus session context
- return assistant text
- keep product-specific reasoning, tool choice, and business rules outside the runtime

## Shell Bridge

Use the shell bridge boundary for:

- local shell execution
- optional remote shell execution
- approval wrappers
- policy enforcement
- alternative transports

If a project needs approvals or sandboxing, put that logic here rather than embedding it in
prompt rendering or slash-command parsing.

## Slash Commands

Projects may add slash commands by subclassing or wrapping the session dispatcher.

When adding commands:

- keep mode management explicit
- keep side effects out of rendering helpers
- record operator-visible actions in the transcript when appropriate

## Rendering

The default renderer uses `rich`, but rendering should stay downstream of execution and routing.

Good extension points:

- custom panels and tables
- status displays
- richer streaming views
- eventual `textual` widgets

Bad extension points:

- mixing tool policy into rendering code
- deriving runtime state from screen layout

## Input Engine

`prompt_toolkit` is the default input engine because it supports:

- async prompting
- multiline input
- completions
- better keyboard handling than a raw readline baseline

If a project swaps the input layer, preserve the same runtime contract.

## Upgrade Path

The expected evolution path is:

1. stabilize the plain REPL loop
2. stabilize transcript/history/shell boundaries
3. improve completions and status views
4. wrap the runtime in a richer TUI only if the product needs it
