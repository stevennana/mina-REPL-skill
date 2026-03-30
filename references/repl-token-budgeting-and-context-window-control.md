# REPL Token Budgeting And Context Window Control

This file defines the recommended token-budgeting and context-window control behavior for
AI-oriented shells built on `mina-repl-core`.

## Evidence Status

- **Verified:** Codex exposes model context and auto-compact configuration, caps compact prompt input, and uses explicit token percentages and fallback limits in its memory pipeline.
- **Verified:** OpenCode exposes `model` and `small_model`, caps output tokens, and uses explicit compaction buffer and prune thresholds.
- **Inferred:** model-aware token policy should be treated as runtime policy, not as an emergent side effect of whichever model happens to be selected.
- **Recommended:** `mina-repl-core`-based shells should publish exact token-budget rules when the upstream sources provide them, and avoid inventing unsupported numeric thresholds when they do not.

## 1. There is no universal numeric cutoff for a "small model"

Neither Codex nor OpenCode defines a universal parameter-count or context-window threshold that
says "models below this size are small."

Instead, both repos use **role-based assignment**:

- Codex assigns specific models to specific jobs
- OpenCode exposes an explicit `small_model` slot for lightweight work

That means a shell should not invent rules like:

- "anything under 20B is small"
- "anything with a 128k window is medium"

If a project wants those categories, it should define them explicitly rather than claiming the
upstream repos already do.

## 2. Exact Codex numbers worth carrying forward

Codex encodes several concrete token-budget values:

- compact user message cap: `20_000` tokens
- stage-1 memory fallback rollout limit: `150_000` tokens
- stage-1 memory rollout budget: `70%` of the active model's effective input window
- stage-1 memory model: `gpt-5.1-codex-mini`
- stage-1 memory reasoning effort: `low`
- stage-2 memory model: `gpt-5.3-codex`
- stage-2 memory reasoning effort: `medium`

These numbers come from:

- `codex-rs/core/src/compact.rs`
- `codex-rs/core/src/memories/mod.rs`
- `codex-rs/core/src/memories/prompts.rs`

The key lesson is that Codex does not try to spend the whole window. It reserves headroom and
uses a smaller model for cheaper summarization-style work.

## 3. Exact OpenCode numbers worth carrying forward

OpenCode also encodes concrete token and compaction limits:

- default output-token cap: `32_000`
- compaction buffer: `20_000`
- prune minimum: `20_000`
- prune protect threshold: `40_000`

OpenCode's compaction logic also computes reserved headroom as:

- `cfg.compaction.reserved`
- otherwise `min(20_000, model max output tokens)`

And the usable context budget becomes:

- `model.limit.input - reserved`
- or, if input limit is not present, `model.limit.context - model max output tokens`

These values come from:

- `packages/opencode/src/provider/transform.ts`
- `packages/opencode/src/session/llm.ts`
- `packages/opencode/src/session/compaction.ts`

OpenCode also exposes a distinct `small_model` role for lightweight work such as title generation,
but does not assign one universal numeric size threshold to that role.

## 4. Efficient context-window control rules

The strongest shared pattern is:

1. keep the current model explicit
2. reserve output headroom
3. compact before overflow
4. preserve active turn state when compacting
5. use a smaller or cheaper model for lightweight subproblems when explicitly configured

In practice, the shell should:

- never treat the full context window as replayable history budget
- reserve room for system/developer instructions
- reserve room for tool schemas and tool-call overhead
- reserve room for expected assistant output
- preserve the current plan/tool/review/workspace state during compaction

## 5. Recommended direct carry-over for `mina-repl-core`

Source-backed best-practice numbers that are safe to document directly:

- use `20_000` as a meaningful order-of-magnitude compaction/output headroom reference
- treat `32_000` as OpenCode's explicit default output-token cap, not a universal constant
- treat `150_000` as Codex's fallback stage-1 rollout ceiling for memory extraction
- treat `70%` as a strong example of reserving non-trivial headroom instead of using the full model window

Recommended interpretation:

- use exact numbers only when they come from explicit source constants or config
- treat them as role-specific and implementation-specific defaults, not universal laws
- prefer explicit per-model policy over one global budget

## 6. Anti-patterns to avoid

Avoid these behaviors:

- assuming a model is "small" from its name alone unless the project explicitly maps that name
- filling the entire context window with history and leaving no output headroom
- waiting for hard overflow before compacting
- compacting away the current active plan/tool/workspace state
- documenting unsupported numeric categories as if the upstream repos defined them
