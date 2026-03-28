# REPL MCP And Tool Registry

This file describes the recommended tool-registry and MCP-facing design for a shell built on
`mina-repl-core`.

## 1. Tools should be discoverable

An advanced shell should make the available tools inspectable.

At minimum, expose:

- tool id
- origin (`builtin`, `mcp`, or local wrapper)
- schema or parameter shape
- approval expectations

## 2. Treat MCP tools as first-class but distinct

MCP tools should not be collapsed into the same conceptual bucket as shell commands.

Guidance:

- keep tool origin explicit
- keep result shape explicit
- preserve approval boundaries per tool class when needed

## 3. Tool loop state belongs in the operator surface

The shell should be able to surface:

- pending tool
- running tool
- completed tool
- failed tool

This matters for both built-in and MCP tools.

## 4. Schema visibility is part of usability

If the shell wants the model to use tools well, it should keep tool schemas visible and stable
enough that downstream agents or clients can reason about them.

## 5. Recommendation

Use a registry model where the shell can:

- list tool ids
- list tool metadata
- route tool calls by id
- attach approval and provenance metadata without hiding it in raw prompt text
