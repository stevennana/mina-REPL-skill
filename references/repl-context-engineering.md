# REPL Context Engineering

This file describes how an agent shell built on `mina-repl-core` should structure context before
the model sees a turn.

## Evidence Status

- **Verified:** Codex uses layered instructions, AGENTS/project-doc precedence, explicit context management, and explicit compaction/memory behavior.
- **Inferred:** tool, review, and plan state should be treated as structured context inputs in a shell.
- **Recommended:** `mina-repl-core` should keep context layers inspectable and intentionally composed.

## 1. Treat context as layers, not one blob

Codex and OpenCode both imply a layered context model.

Recommended layers:

- system/base instructions
- developer/runtime instructions
- project-doc instructions
- session memory and summaries
- current turn state
- tool/review/plan state
- user prompt

Do not flatten these into one undifferentiated prompt string in the implementation model.

## 2. Keep stable and dynamic context separate

Stable context:

- base instructions
- AGENTS/project-doc rules
- long-lived model configuration
- durable workflow policies

Dynamic context:

- current draft
- active plan or todo state
- pending approvals
- active tool loop state
- current review/diff context

This separation makes compaction, caching, and debugging tractable.

## 3. Project docs are context, not chat

Codex's AGENTS layering shows that repo-local guidance is a structured instruction source with
scope and precedence.

Guidance:

- treat project docs as a dedicated instruction layer
- preserve scope and precedence
- do not mix them into plain conversation history

## 4. Context engineering should preserve reviewability

A good shell should let an operator reason about where model behavior came from.

That means:

- the major context layers are knowable
- the active model/provider is knowable
- compaction is visible
- plan/build state is visible
- project-doc layers are visible

## 5. Context budget is a policy surface

Codex models context-window constraints explicitly.

Guidance:

- reserve headroom for system prompt, tool overhead, and model output
- summarize intentionally when the thread grows large
- prefer navigational summaries over lossy opaque truncation
- treat compaction as a policy decision, not a hidden cleanup step
- tie budgets to the selected model instead of assuming one universal usable window

Source-backed examples worth documenting directly when relevant:

- Codex memory stage 1 uses `70%` of the active model's effective input window
- Codex memory stage 1 falls back to `150_000` tokens when model window metadata is unavailable
- Codex caps compact user-message input at `20_000` tokens
- OpenCode defaults its output-token cap to `32_000`

## 6. Prefer structured state over prompt stuffing

Whenever possible, keep state in structured forms first:

- session metadata
- plan/todo state
- tool state
- approval state
- review state

Then render only the relevant subset into the model-visible context.

This reduces accidental prompt bloat and keeps the shell inspectable.
