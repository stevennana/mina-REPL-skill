# REPL Project Root And Repo Scouting

This file defines the recommended project-root discovery and repository-scouting behavior for
AI-oriented shells built on `mina-repl-core`.

## Evidence Status

- **Verified:** Codex treats repo instructions such as `AGENTS.md`, workspace structure, and install/build metadata as first-class context before implementation work begins.
- **Verified:** OpenCode treats project config, root discovery, and list/glob/read/grep tools as core parts of how an agent understands a workspace.
- **Inferred:** an effective AI shell should understand the project root and its metadata before reading arbitrary deep source files.
- **Recommended:** `mina-repl-core`-based shells should make repo scouting a deliberate first phase of local reasoning.

## 1. Start at the project root

Before deep file reads, the shell should identify:

- the current working directory
- the nearest repository or project root
- whether a VCS root exists
- the top-level directories and key root files

This gives the shell an explicit anchor for later phrases like:

- "this repo"
- "the current project"
- "the root config"
- "the build file"

## 2. Read root metadata before deep code

The shell should inspect root-level metadata files early because they often explain the project's
meaning, tooling, and expected workflows better than random source files do.

Typical high-value files:

- `README*`
- `AGENTS.md`
- `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, or equivalent build manifests
- `Makefile`, `justfile`, task runners, and lockfiles
- project config like `opencode.json`, `.opencode/`, `.codex/`, `.env.example`, or similar
- root `docs/` or architecture notes when present

The goal is to infer:

- what kind of project this is
- how it is built and tested
- what instructions govern the repo
- what root-level config changes behavior

## 3. Use a repo-scouting ladder

The normal order should be:

1. identify cwd and nearest project root
2. inspect the top-level tree
3. read root metadata and manifests
4. narrow with `glob` and `grep`
5. read relevant deeper files
6. use broader shell execution only when simpler discovery is insufficient

This reduces blind exploration and keeps later reasoning grounded in the actual project shape.

## 4. Prefer non-interactive discovery tools

For agent-driven repo scouting, prefer tools and commands that produce stable, transcriptable output.

Good defaults:

- `list` or directory reads
- `glob`
- `grep`
- `read`
- shell fallbacks like `rg --files`, `find`, `sed -n`, `head`, `tail`, and focused `awk`

Avoid interactive pagers like `less` as a default agent step because they are:

- harder to automate
- harder to transcript and replay
- worse for deterministic reasoning than direct bounded reads

`less` can still be useful for a human operator, but it is usually not the right default inside an
autonomous agent loop.

## 5. Infer meaning from manifests before symbols

Before searching deep implementation symbols, the shell should infer the project's shape from
manifests and root config:

- language and package manager
- runtime or framework
- test and build entrypoints
- repo-local instructions
- service-specific config directories

This prevents the shell from guessing the stack or inventing workflows that the root metadata
already explains.

## 6. Use `grep` and `awk` intentionally

When shell fallbacks are needed:

- use `grep` or `rg` to find specific metadata keys, scripts, commands, or instruction phrases
- use `awk` only for lightweight structured extraction, such as listing columns or specific keys
- keep shell parsing narrow and readable

Do not turn repo scouting into brittle ad hoc shell scripting when direct read/search tools or a
small bounded command would answer the question more safely.

## 7. Anti-patterns to avoid

Avoid these behaviors:

- diving into deep source files before understanding the root tree
- inferring the stack without reading root manifests
- ignoring `README` or `AGENTS.md` and then asking the user basic repo questions
- replying with "please run `ls`" when the shell could inspect the tree itself
- using interactive pagers as the default inspection path
- writing exploratory scripts just to learn what a bounded read or search could reveal
