# Integration Guide

This file is the repo-facing integration summary.
For the deeper contracts, read:

- `references/repl-runtime-contract.md`
- `references/repl-context-engineering.md`
- `references/repl-prompt-composition.md`
- `references/repl-memory-and-model-config.md`
- `references/repl-prompt-templates.md`
- `references/repl-mcp-and-tool-registry.md`
- `references/repl-tool-selection-and-usage.md`
- `references/repl-tool-loop-and-turn-orchestration.md`
- `references/repl-plan-execution.md`
- `references/repl-approval-and-autonomy.md`
- `references/repl-session-lifecycle.md`
- `references/repl-plan-build-modes.md`
- `references/repl-terminal-ui-best-practices.md`

## Install

```bash
pip install -e .[dev]
```

Optional extras:

```bash
pip install -e .[dev,ssh,textual,cmd2]
```

## Basic wiring

```python
from mina_repl_core import LocalShellBridge, ReplCoreSession


async def my_agent(user_text: str, session: ReplCoreSession) -> str:
    return "your result"


session = ReplCoreSession(
    assistant=my_agent,
    shell_bridge=LocalShellBridge(),
    history_path="~/.myproject/history.txt",
    transcript_path="~/.myproject/session.jsonl",
)
```

## Integration rule

Keep domain logic and project-specific policy above the runtime layer.
Use `ReplCoreSession` as the adapter, not as the application brain.

## Canonical asset files

If your project ingests the skill metadata directly, read the repo-root files:

- `manifest.yaml`
- `contracts.yaml`
- `best_practices.yaml`
- `sources.yaml`
