# REPL LLM Logging And Observability

This file defines the recommended logging strategy for debugging LLM communication in an
agent shell built on `mina-repl-core`.

## Evidence Status

- **Verified:** Codex documents explicit tracing and debug toggles (`DEBUG=true`, `RUST_LOG`, `log_dir`) and emits bounded vs trace-level tool diagnostics.
- **Verified:** OpenCode’s session LLM layer and processor log model/provider/session identifiers and stream lifecycle events, and its contributing guide recommends terminal-first debugger attachment for the live server/TUI flow.
- **Inferred:** debugging LLM communication requires layered observability, not a single “dump the whole request” switch.
- **Recommended:** `mina-repl-core` shells should expose a bounded default logging mode plus an opt-in deep trace mode for request/response debugging.

## 1. Log at three levels

### Default operational logs

Always keep lightweight logs for:

- session id
- turn id
- provider id
- model id
- agent mode
- approval mode
- active tool
- turn phase transitions

These logs should be safe to keep on during normal operator use.

### Debug logs

Enable richer debugging when explicitly requested:

- prompt layer composition summary
- tool selection decisions
- approval pause reasons
- compaction events
- token or context-budget summaries
- model-selected output-token limit and reserved headroom

These should still avoid dumping raw secrets or giant payloads by default.

### Trace logs

Use trace-level logs only for deep debugging:

- exact request/response payload fragments
- streamed reasoning/tool event boundaries
- raw tool result objects when needed
- provider-specific options and headers after redaction

Trace logging should be opt-in and clearly scoped.

## 2. Keep logs keyed by shell identity

Every meaningful log line should be attributable to:

- session id
- turn id
- provider id
- model id
- tool call id when relevant

Without stable identifiers, LLM debugging becomes guesswork once multiple turns overlap.

## 3. Separate prompt logging from transcript logging

Do not treat transcript export as equivalent to model-debug logging.

Keep these separate:

- transcript: operator-facing session record
- prompt composition log: what layers were assembled for the model
- LLM communication log: request/response lifecycle and stream events

## 4. Redact by default

A useful shell should never require unsafe logging to be usable.

Default logging must:

- redact secrets and tokens
- avoid raw environment dumps
- avoid full prompt dumps unless explicitly enabled
- avoid leaking raw sensitive tool output

## 5. Log stream lifecycle explicitly

For model-streaming shells, useful events include:

- turn started
- request sent
- stream started
- reasoning started / delta / ended
- tool call started / completed / failed
- stream error
- compaction started / finished
- turn completed / interrupted

This mirrors the shape used by Codex and OpenCode more closely than a single “model replied” line.

## 6. Use bounded summaries first

Codex’s `js_repl` logging is a good model:

- `info` level emits bounded summaries
- `trace` level emits the exact serialized object

Apply the same pattern to shell-agent logging:

- default to bounded summaries
- allow exact payload traces only in explicit deep-debug mode

## 7. Keep a stable log sink strategy

A practical shell should support:

- a known default log file location
- an override for one-off debug runs
- terminal-first debugging during local development

This makes incident reproduction much easier than relying on ephemeral stdout only.

## 8. Practical recommendation for `mina-repl-core`

For a Python implementation, provide:

- normal logs for session/turn/tool state
- debug logs for prompt composition and tool routing
- trace logs for raw LLM communication after redaction
- per-run log directory overrides for focused debugging
- stable correlation ids across transcript, approvals, tool activity, and LLM events
- model-aware budget events such as "small model used", "compaction threshold crossed", and "reserved headroom applied"
