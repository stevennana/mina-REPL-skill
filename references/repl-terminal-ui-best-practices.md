# REPL Terminal UI Best Practices

This file captures terminal-shell UI guidance extracted from `openai/codex` and
`anomalyco/opencode`.

Use it when a project built on `mina-repl-core` needs a stronger operator-facing shell UI.

## 1. Treat the TUI as one client of the runtime

A terminal UI can be the primary experience without being the whole architecture.

Guidance:

- keep session, shell, transcript, and tool logic outside the view layer
- allow the runtime to support headless or alternate clients later
- avoid coupling core behavior to one screen layout

## 2. Keep important state visible

A serious agent shell should expose the current state clearly:

- runtime mode: `chat`, `shell`, `multiline`
- operational mode: `plan`, `build`
- approval/autonomy mode
- session title or identity
- review/diff availability

Do not hide these behind implicit defaults only.

## 3. Preserve a review surface after mutations

After file-changing actions, the shell should make review state obvious:

- changed files
- diff or review availability
- whether VCS is enabled
- whether snapshots or review data are available

This should remain a first-class UI surface, not only a hidden command.

## 4. Use progressive disclosure in the interface

Keep the main interaction area focused, then use dialogs, side panels, and status views for:

- session management
- permissions
- models/providers
- skills
- review state
- file/context views

This keeps the shell dense without becoming noisy.

## 5. Separate planning from execution visually

If the shell supports read-only planning and mutating build behavior:

- make the current behavior visible
- make the transition explicit
- do not present a mutating shell as if it were still planning

This is a UI concern as much as a prompt-contract concern.

## 6. Keep permission UX honest

If the shell asks for approval before actions:

- show that clearly in the UI
- show when auto-accept or higher-autonomy modes are active
- do not imply that approval prompts equal sandboxing

The operator should understand whether the shell is confirmation-gated, policy-gated, or truly isolated.

## 7. Prefer stable terminal styling

Codex's TUI style guidance is intentionally conservative:

- headers: `bold`
- primary text: default foreground
- secondary text: `dim`
- tips, selection, status indicators: `cyan`
- success and additions: `green`
- errors, failures, deletions: `red`
- assistant/brand identity: `magenta`

Avoid custom colors unless there is a strong reason. Prefer styles that survive different terminal themes.

## 8. Favor keyboard-first control surfaces

Terminal shells should make keyboard workflows obvious and complete.

Good control surfaces include:

- slash commands
- command palettes
- dialogs with explicit keybinds
- predictable focus movement

Do not rely on pointer interactions for core workflows.

## 9. Keep terminal testing and debugging practical

Terminal UI behavior should be testable and debuggable as a real interactive system:

- support interactive startup
- keep logs and trace output easy to enable
- avoid brittle input sequencing assumptions
- keep testing instructions explicit for operators and contributors

## 10. Practical synthesis for `mina-repl-core`

For a Python agent shell, the most transferable UI rules are:

- runtime and UI are separate layers
- operator state must stay visible
- review/diff state deserves dedicated UI
- plan/build and approval modes should be explicit
- terminal styling should be restrained and legible
- keyboard-first interaction should remain complete
