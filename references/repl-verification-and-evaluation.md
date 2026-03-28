# REPL Verification And Evaluation

This file describes how to verify that an agent shell built on `mina-repl-core` is behaving well.

## 1. Verify more than code execution

A good shell should be evaluated across:

- runtime correctness
- tool-loop correctness
- approval behavior
- session/review behavior
- operator-visible UI behavior

## 2. Recommended evaluation layers

### Contract checks

- root skill files exist
- packaged YAML mirrors stay in sync
- manifest/contracts expose the documented concepts

### Replay and transcript checks

- transcript export remains stable
- history recall behavior remains intelligible
- compaction markers are visible when applicable

### Operator-surface checks

- approval mode is visible
- plan/build state is visible
- review state is visible after mutations

### UI validation

- for TUI changes, preserve screenshots, recordings, or snapshot-style evidence when possible

## 3. Verification rule

Do not treat "the shell ran a command" as sufficient validation.
The product contract includes operator comprehension and recoverability too.
