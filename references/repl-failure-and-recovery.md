# REPL Failure And Recovery

This file describes recovery paths an agent shell should model explicitly.

## Common Recovery Paths

- interrupt the current turn
- deny an approval and continue safely
- recover from a failed tool call
- re-enter planning after a bad execution path
- fork from an earlier session point
- compact and continue when context grows too large
- review and revert after mutations when the shell supports that behavior

## Principles

- recovery should be explicit, not improvised
- operator-visible state should explain what failed
- recovery actions should preserve session continuity when possible
- the shell should not silently discard important state during recovery

## Minimum Expectation

If the shell supports long-running turns or mutating behavior, it should define:

- how to stop work
- how to retry
- how to step back
- how to preserve context while recovering
