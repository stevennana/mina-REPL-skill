# REPL Orchestrator Guidance

This file defines the orchestrator layer for an AI-oriented shell built on `mina-repl-core`.

## Evidence Status

- **Verified:** Codex has a dedicated tool orchestrator and explicit thread/turn protocol; OpenCode has a session processor, LLM loop, tool context, and visible session status handling.
- **Inferred:** an AI shell needs one coordinating layer that owns turn execution rather than scattering those decisions across the prompt widget, slash commands, and tool adapters.
- **Recommended:** `mina-repl-core`-based shells should make the orchestrator the center of model-driven execution.

## What The Orchestrator Owns

The orchestrator is responsible for:

- starting a user turn
- assembling model-visible context
- selecting the model call path
- interpreting tool decisions
- pausing for approval when policy requires it
- invoking the right tool or shell adapter
- feeding tool results back into the model
- deciding whether the turn continues, pauses, retries, or completes
- surfacing turn/tool/approval state to the transcript and status surfaces

## What The Orchestrator Does Not Own

The orchestrator should not become:

- the prompt widget
- the shell command runner
- the transcript store
- the slash-command parser
- the tool registry itself

It coordinates these systems; it does not replace them.

## Canonical Turn Loop

For an AI-oriented shell, the normal turn loop is:

1. user submits a natural-language turn
2. orchestrator builds model-visible context
3. model responds with either text, a tool call, or more structured state
4. orchestrator checks whether approval is needed
5. tool executes if allowed
6. result is returned to the model
7. model either continues or completes the turn

This is the default shell behavior. The operator should not need to manually enter shell mode for the AI to use shell tools.

## Operator-Visible Orchestrator State

A stronger shell should be able to show:

- current turn id
- current phase
- active tool
- waiting for approval
- interrupted / retrying / compacting

The shell should not feel like a black box during long-running or tool-heavy turns.

## Natural-Language-First Rule

The primary operator model should be:

- type a request naturally
- let the shell decide whether to call tools
- respond to approval prompts only when needed

`/run` remains a power-user override for explicit manual shell execution.

`/mode` may still exist as a low-level runtime control, but it should not be part of the normal happy path for an AI shell.
