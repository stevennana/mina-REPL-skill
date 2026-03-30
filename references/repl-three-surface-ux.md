# REPL Three-Surface UX

This file defines the recommended three-surface shell layout for an AI REPL built on
`mina-repl-core`.

## Evidence Status

- **Verified:** Codex separates transcript/history concerns from the chat composer and uses a dedicated footer/status-line system in the bottom pane.
- **Verified:** OpenCode separates the message timeline, composer/docks, and footer/sidebar/status surfaces across its session UI.
- **Inferred:** a shell becomes easier to reason about when transcript, draft input, and ambient status each have a clear ownership boundary.
- **Recommended:** `mina-repl-core` implementations should treat these as three primary UX surfaces.

## 1. Transcript Surface

The transcript surface owns what already happened.

It should include:

- user and assistant history
- tool activity and progress
- plan/todo progress when relevant
- approvals and review state when relevant
- workspace discovery activity and resolved local targets when relevant
- compact summaries or recovery markers when they affect session understanding

Design rules:

- make it scrollable and replayable
- keep row types visually distinct
- show running work as explicit in-progress rows instead of hiding it
- preserve export or transcript-copy workflows

The transcript surface should answer:

- what happened
- what is still running
- what changed

## 2. Chatting Surface

The chatting surface owns what the user is preparing now.

It should include:

- text draft
- multiline editing behavior
- slash-command entry and expansion
- history recall for drafts
- paste handling
- attachment or contextual insertions when supported

Design rules:

- treat the composer as a state machine, not a plain textbox
- keep draft state separate from transcript state
- avoid accidental submission during paste bursts or multiline entry
- preserve explicit submit vs queue semantics when the shell supports them
- keep the operator’s main path natural-language-first; the composer should not force manual shell-mode switching before the AI can use tools

The chatting surface should answer:

- what am I about to send
- what routing or draft behavior applies to this submission, if any
- what will happen if I submit now

## 3. Footer Surface

The footer surface owns what the operator should know right now.

It should include either:

- instructional hints when the shell needs operator action
or
- compact contextual status when the shell is idle enough to show ambient state

Useful footer/status content includes:

- available shortcuts or command hints
- current model
- context usage
- current working directory
- git branch or review state
- connected MCP/app/tool status
- whether the orchestrator is waiting for approval, waiting for the model, or running a tool

Design rules:

- keep footer rendering pure; selection of what to show belongs in higher-level state
- collapse gracefully on narrow terminals
- prefer the most actionable hint over ambient metadata when space is constrained
- do not duplicate transcript content here

The footer surface should answer:

- what should I know right now
- what can I do next quickly

When the shell auto-runs safe discovery, transcript and footer should make it obvious that the
agent inspected the workspace on the user's behalf rather than merely suggested a command.

## 4. Surface Ownership Rule

Keep these boundaries clean:

- transcript = what happened
- chatting = what is being prepared
- footer = what the operator should know now

The orchestrator owns when the shell moves from user intent to tool execution. That state should be reflected across transcript and footer surfaces, not offloaded to manual `/mode` changes.

If the UI makes users think they must switch modes before the AI can inspect files, run commands, or continue a tool turn, the shell is leaking runtime internals into the primary UX.

Do not let:

- footer become a second transcript
- composer become a hidden status bar
- transcript become the only place to discover active mode or status

## 5. Graceful Implementation Pattern

For a practical Python shell:

1. render the transcript as the primary timeline
2. render the composer as the dedicated bottom interaction region
3. render a lightweight footer/status line beneath or alongside the composer
4. elevate review, permission, and todo details into docks, panels, or overlays when needed

This keeps the shell understandable even as more features are added.
