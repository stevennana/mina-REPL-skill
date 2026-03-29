# Mina REPL Core

`mina-repl-core` is a root-level Codex skill and a Python package for building REPL-first AI
terminal applications in Python.

This repository is intentionally a hybrid:

- the repo root is the skill root, so it can be symlinked directly into `$CODEX_HOME/skills/`
- `src/mina_repl_core/` contains the reusable Python runtime package
- `references/` contains the canonical deep guidance the skill should read when it triggers
- `docs/` contains lighter repo-facing summaries for contributors and integrators

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

## What The Runtime Owns

`mina-repl-core` is the reusable runtime layer. It owns:

- multi-turn prompt lifecycle
- explicit `chat`, `shell`, and `multiline` modes
- slash-command routing
- transcript and history persistence
- shell execution through a dedicated bridge
- structured terminal rendering

It should not be the place where project-specific business logic, approval policy, or product
workflows live.

For AI-oriented shells, users should normally type natural-language requests; tool and shell selection should happen through the orchestrator, with approval pauses when required.

## Canonical Reading Order

If you are using this repo as a skill, read in this order:

1. `SKILL.md`
2. `references/repl-runtime-contract.md`
3. `references/repl-context-engineering.md`
4. `references/repl-prompt-composition.md`
5. `references/repl-memory-and-model-config.md`
6. `references/repl-tool-loop-and-turn-orchestration.md`
7. `references/repl-plan-execution.md`
8. `references/repl-prompt-templates.md`
9. `references/repl-mcp-and-tool-registry.md`
10. `references/repl-tool-selection-and-usage.md`
11. `references/repl-orchestrator-guidance.md`
12. `references/repl-approval-and-autonomy.md`
13. `references/repl-session-lifecycle.md`
14. `references/repl-plan-build-modes.md`
15. `references/repl-architecture.md`
16. `references/repl-extension-points.md`
17. `references/repl-terminal-ui-best-practices.md`
18. `references/repl-verification-and-evaluation.md`
19. `references/repl-failure-and-recovery.md`
20. `references/repl-maturity-matrix.md`
21. `references/repl-source-traceability.md`
22. `references/repl-subsystem-map-codex.md`
23. `references/repl-subsystem-map-opencode.md`
24. `references/repl-source-baseline.md`
25. `references/repl-design-opencode.md`

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
