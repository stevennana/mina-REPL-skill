# Mina REPL Core

`mina-repl-core` is a Codex skill and a Python package for building AI REPL shells in Python.

In simple terms, this project helps you build a terminal-based AI agent that can:

- accept normal natural-language requests
- keep multi-turn session history
- run tools and shell commands through a controlled runtime
- show transcript, status, and tool activity clearly
- grow from a simple REPL into a richer terminal UI later

This repository is intentionally a hybrid project:

- the repo root is the skill root, so it can be symlinked directly into `$CODEX_HOME/skills/`
- `src/mina_repl_core/` contains the reusable Python runtime package
- `references/` contains the canonical deep guidance the skill should read when it triggers
- `docs/` contains lighter repo-facing summaries for contributors and integrators

## Where The Guidance Comes From

The best-practice guidance in this project is based mostly on the **source code and docs** of:

- OpenAI `codex`
- `anomalyco/opencode`

This is an important point: the guidance here is not just generic REPL advice. It is largely
extracted from how those projects actually model:

- orchestrator-driven tool use
- context and prompt layering
- approvals and visible turn state
- repo discovery and workspace awareness
- token budgeting, compaction, and model-aware context control
- terminal UX patterns for transcript, input, and footer/status surfaces

This project translates those ideas into a Python-focused skill and runtime foundation.

## What This Project Is

Use `mina-repl-core` when you want a reusable base for an AI shell, not when you want to encode
one product's domain-specific business logic.

`mina-repl-core` is responsible for runtime concerns such as:

- prompt lifecycle
- internal routing state
- transcript and history persistence
- shell/tool bridge boundaries
- structured terminal rendering
- REPL-first extension points

It is **not** the place to hard-code:

- product-specific workflows
- business rules
- domain-specific troubleshooting logic
- one team's repo conventions

## Skill Layout

```text
mina-repl-core/
  SKILL.md
  manifest.yaml
  contracts.yaml
  best_practices.yaml
  sources.yaml
  agents/openai.yaml
  references/
  docs/
  examples/
  src/mina_repl_core/
  tests/
  tools/
```

## Install As A Codex Skill

### 1. Clone the repository

```bash
git clone <YOUR-REPO-URL> mina-repl-core
cd mina-repl-core
```

### 2. Symlink the repo root into your Codex skills directory

Default Codex home:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)" ~/.codex/skills/mina-repl-core
```

If you use `CODEX_HOME`:

```bash
mkdir -p "$CODEX_HOME/skills"
ln -s "$(pwd)" "$CODEX_HOME/skills/mina-repl-core"
```

### 3. Restart Codex if it is already running

Codex should now see this repository itself as the `mina-repl-core` skill.

## Install As A Python Package

### Prerequisites

- Python 3.10 or newer
- `pip`
- `git`

### 1. Create a virtual environment

macOS and Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### 2. Install the package

Base install:

```bash
pip install -e .
```

Full local-development install:

```bash
pip install -e .[dev,ssh,textual,cmd2]
```

### 3. Run the demo REPL

```bash
python -m mina_repl_core
# or
mina-repl-core
```

### 4. Verify the install

```bash
python tools/sync_skill_assets.py --check
python -m unittest discover -s tests -q
```

## How To Think About It

For AI-oriented shells, the intended operator experience is:

- the user types natural-language requests
- the orchestrator decides when to inspect files, use tools, or ask for approval
- the shell shows what happened in the transcript and status surfaces
- manual commands like `/run` stay available, but they are not the main workflow

That means `chat`, `shell`, and `multiline` are runtime mechanics, not the main UX the user should
have to manage directly.

It also means:

- the shell should inspect the current workspace itself when the next safe read-only step is obvious
- the shell should understand the project root and root metadata early
- token usage should be controlled with model-aware headroom and compaction rather than by filling the entire context window

## Canonical Reading Order

If you are using this repo as a skill, start here:

1. `SKILL.md`
2. `references/repl-runtime-contract.md`
3. `references/repl-context-engineering.md`
4. `references/repl-prompt-composition.md`
5. `references/repl-memory-and-model-config.md`
6. `references/repl-token-budgeting-and-context-window-control.md`
7. `references/repl-discovery-and-workspace-awareness.md`
8. `references/repl-project-root-and-repo-scouting.md`

Then continue into the other `references/` files as needed.

If you want to verify where the guidance came from, read:

- `references/repl-source-traceability.md`
- `references/repl-subsystem-map-codex.md`
- `references/repl-subsystem-map-opencode.md`
- `references/repl-source-baseline.md`

## Example Import

```python
import asyncio

from mina_repl_core import LocalShellBridge, ReplCoreSession


async def my_agent(user_text: str, session: ReplCoreSession) -> str:
    return f"Agent received: {user_text}"


async def main() -> None:
    session = ReplCoreSession(
        assistant=my_agent,
        shell_bridge=LocalShellBridge(),
        history_path="~/.mina_repl_core/history.txt",
        transcript_path="~/.mina_repl_core/session.jsonl",
    )
    await session.run()


if __name__ == "__main__":
    asyncio.run(main())
```
