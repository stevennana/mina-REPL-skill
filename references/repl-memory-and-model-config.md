# REPL Memory And Model Config

This file defines the recommended memory and model-configuration policies for agent shells built
on top of `mina-repl-core`.

## Evidence Status

- **Verified:** Codex separates persistent history from richer local composer state and has a dedicated memory subsystem; OpenCode exposes provider/model state explicitly in session shapes.
- **Inferred:** long-term shell memory should include project-doc layers and compacted summaries.
- **Recommended:** `mina-repl-core` should model memory and model config as operator-visible policy surfaces.

## 1. Separate short-term and long-term memory

Do not treat "memory" as one blob.

Recommended split:

- short-term memory
  - current draft
  - local session recall
  - current turn context
  - active review state
- long-term memory
  - persisted history
  - compacted session summaries
  - repo-local project docs
  - operator configuration and model defaults

## 2. Persistent history is not the same as local draft history

Codex's TUI composer distinguishes:

- persistent cross-session history
- richer local in-session history with more state

Guidance for Python REPL shells:

- keep persistent history stable and lightweight
- allow richer in-session state without forcing all of it into on-disk history
- document exactly what is restored from each memory layer

## 3. Use project docs as structured long-term guidance

Codex layers `AGENTS.md` top-down:

- global
- repo root
- subdirectory

Guidance:

- treat repo-local docs as long-term working memory for the shell
- keep their precedence explicit
- distinguish operator instructions from conversation history

## 4. Compaction and summarization should be explicit

Long-running sessions need explicit summary behavior.

Guidance:

- summarize intentionally, not by silent truncation
- preserve a compacted summary artifact or marker
- make the operator aware when context was compacted
- keep compaction distinct from history deletion

## 5. Keep model config explicit and operator-visible

OpenCode and Codex both expose provider/model configuration rather than hiding it in code.

Recommended operator-visible model config includes:

- provider id
- model id
- small-model id when one exists
- max output token limit when the runtime knows it
- reasoning or effort level when relevant
- variant or system prompt source when relevant

The operator should be able to tell what model is currently driving the shell.

## 6. Provider-agnostic shells still need clear defaults

Provider-agnostic design is useful, but only if defaults are still obvious.

Guidance:

- keep provider/model selection explicit
- keep per-provider overrides explicit
- avoid surprising implicit model switches
- document when a model change affects shell behavior such as image support or reasoning level
- document when a smaller or cheaper model is used for lightweight tasks such as summaries or titles
