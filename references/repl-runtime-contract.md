# REPL Runtime Contract

This file is the canonical deep guidance for the operator-visible behavior of `mina-repl-core`.

## Primary Goal

Provide a reusable Python-native REPL runtime that can host an agent cleanly without collapsing
chat, shell, and drafting into one ambiguous stream.

## Core Invariants

- The runtime owns the prompt loop.
- The runtime keeps `chat`, `shell`, and `multiline` as explicit modes.
- Shell execution is a separate tool channel, not just another assistant message.
- History and transcripts are durable runtime concerns, not optional debugging extras.
- Rendering is structured so the UI layer can evolve without breaking the runtime contract.

## Operator-Visible Modes

### `chat`

- User input is routed to the assistant callback.
- Assistant output is rendered as assistant content, not shell output.

### `shell`

- User input is executed through the shell bridge.
- Results must remain structured and auditable.
- The bridge should expose at least:
  - command
  - exit code
  - stdout
  - stderr
  - timing metadata

### `multiline`

- User input is buffered as multiline prompt input before submission.
- Multiline behavior should be explicit, not accidental.

## Slash Command Contract

The base runtime should keep an explicit control surface for mode switching and introspection.

The current built-in commands are:

- `/help`
- `/mode <chat|shell|multiline>`
- `/status`
- `/history [n]`
- `/sources`
- `/skill`
- `/run <shell command>`
- `/transcript [path]`
- `/clear`
- `/quit`

If a project adds commands, those commands should preserve the same separation between routing,
execution, rendering, and transcript recording.

## Transcript And History Contract

- History improves operator ergonomics and should be on by default when a path is provided.
- Transcripts improve reproducibility, debugging, and tests.
- Transcript entries should preserve:
  - timestamp
  - role
  - mode
  - content
  - optional metadata
- Shell transcript metadata should at minimum preserve exit code and timing.

## Shell Boundary And Approval Boundary

`mina-repl-core` intentionally stops at the shell bridge boundary.
It does not implement a full approval or sandbox policy on its own.

If a project needs command approvals, restricted execution, or policy enforcement:

- wrap or replace the shell bridge
- keep the approval decision outside the prompt loop
- avoid mixing safety policy with renderer or transcript code

This mirrors the Codex design principle that autonomy policy is a separate layer from the basic
interactive terminal loop.

## Error And Exit Semantics

- `KeyboardInterrupt` should cancel current input rather than crash the runtime.
- `EOFError` should exit the session cleanly.
- Empty input should be ignored without creating noisy transcript state.

## Default Python Stack

- `prompt_toolkit` for prompt handling
- `rich` for rendering
- `asyncio` for concurrency
- optional `asyncssh` for remote shell transport
- optional `textual` as a wrapper once the loop is stable
