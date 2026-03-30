# REPL Discovery And Workspace Awareness

This file defines the recommended workspace-awareness and autonomous-discovery behavior for
AI-oriented shells built on `mina-repl-core`.

## Evidence Status

- **Verified:** Codex emphasizes inspect-first repo exploration, explicit orchestrator control, and tool choice based on the cheapest sufficient action.
- **Verified:** OpenCode's prompt and tool docs explicitly push the agent toward `read`, `glob`, and `grep` style discovery before broader shell use.
- **Inferred:** a useful AI shell should inspect the local workspace itself before asking the operator to type obvious read-only commands.
- **Recommended:** `mina-repl-core`-based shells should treat startup workspace context and safe discovery as first-class orchestrator concerns.

## 1. Treat startup cwd as default workspace context

Unless the user names another target, the shell should treat the startup working directory as the
default workspace or investigation target.

That context should be:

- durable in session metadata
- visible in status output
- available to prompt composition
- overridable when the user provides a more specific path or target

This lets the user say "here", "this directory", or "this project" without restating the path.

## 2. Discover before asking the user

If the next safe read-only step is obvious, the orchestrator should do it itself.

Examples:

- inspect the current directory
- identify likely evidence files or bundles
- confirm whether a named file or path exists
- narrow the local target before asking follow-up questions

The shell should not respond with tutorial prose like "run `ls -la`" or "create a script to inspect
the directory" when the orchestrator could perform that step safely.

## 3. Use a discovery ladder

The normal discovery order should be:

1. reuse workspace and session context already known
2. inspect cheap local metadata or directory contents
3. narrow with `glob`, `grep`, and `read` style tools
4. use broader shell execution only when specialized discovery is insufficient
5. ask the user only when ambiguity or approval blocks progress

This keeps discovery cheap, reviewable, and minimally interruptive.

## 4. Summarize facts before proposing the next step

After a discovery step, the shell should tell the operator:

- what it observed
- what it inferred
- what next safe action it is taking or recommending
- what remains uncertain

The goal is not silent background work. The goal is to minimize unnecessary operator intervention
while keeping the shell legible.

## 5. Ask only on ambiguity or approval boundaries

The shell should interrupt the user only when:

- multiple plausible targets exist
- the next step would cross an approval boundary
- the workspace evidence is insufficient to choose safely
- the user asked for a specific manual workflow

Absent those cases, discovery should remain agent-driven.

## 6. Keep discovery transcript-first

Discovery work should appear as tool activity and observed facts in the transcript, not only as
assistant prose.

A stronger shell will show:

- which workspace or directory it inspected
- which tool or discovery step ran
- what target it resolved
- what the next phase is

This makes the shell feel like an agent instead of a tutor handing back shell snippets.

## 7. Anti-patterns to avoid

Avoid these behaviors in AI-oriented shells:

- telling the user to run `pwd`, `ls`, or `find` for obvious safe discovery
- making `/run` the normal path for initial workspace inspection
- requiring `/mode shell` before the AI can inspect the local workspace
- asking the user to restate the current directory when startup cwd is already known
- broad shell execution before cheap read-only discovery
