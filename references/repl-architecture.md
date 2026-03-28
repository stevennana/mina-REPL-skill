# REPL Architecture

`mina-repl-core` is organized as a skill root plus a Python package.

## Skill Root

The repo root is the skill root:

- `SKILL.md`
- `manifest.yaml`
- `contracts.yaml`
- `best_practices.yaml`
- `sources.yaml`
- `agents/openai.yaml`
- `references/`

This makes the repository directly symlinkable into `$CODEX_HOME/skills/mina-repl-core`.

## Python Runtime Package

The runtime code lives under `src/mina_repl_core/`.

Primary modules:

- `session.py` owns the prompt loop, mode routing, slash commands, and rendering orchestration
- `shell.py` owns local and remote command execution
- `transcript.py` owns durable transcript records and export
- `manifest.py` loads packaged YAML assets
- `demo.py` provides a minimal runnable entrypoint

## Asset Flow

- The repo root YAML files are the canonical editable skill assets.
- `tools/sync_skill_assets.py` mirrors them into `src/mina_repl_core/data/`.
- The runtime package reads the mirrored copies so installs still have the bundled skill data.

## Control Flow

1. prompt for input
2. normalize and classify the input
3. if slash command, dispatch to runtime control logic
4. else if shell mode, execute through the shell bridge
5. else call the assistant callback
6. render structured output
7. record transcript state

## Layering Rule

Use the runtime as an adapter layer.
Keep domain orchestration, business tools, and product policy in higher-level code above it.
