# REPL Prompt Templates

This file defines the recommended prompt-template set for an agent shell built on `mina-repl-core`.

## Core Template Set

Keep these prompt layers distinct and reusable:

- base/system instructions
- developer/runtime instructions
- project-doc instructions
- compact prompt
- plan-mode instructions
- build-mode instructions

## Base/System Template

Owns:

- shell identity
- stable safety posture
- high-level task execution rules
- tool availability framing

It should not own repo-specific conventions or current-turn details.

## Developer/Runtime Template

Owns:

- runtime-specific editing rules
- shell workflow guidance
- response formatting expectations
- operator interaction style

This is where shell-specific behavior belongs, not inside the user turn.

## Compact Prompt Template

Owns the rules for summarizing long sessions while preserving:

- user intent
- active plan state
- unresolved decisions
- tool/review state that still matters

## Plan Template

Owns:

- read-only constraints
- planning responsibilities
- clarification expectations
- plan-output quality expectations

## Build Template

Owns:

- mutating execution permissions
- verification expectations
- transition out of planning mode

## Template Rule

Do not hand-build these as ad hoc string concatenations scattered across the codebase.
Treat them as explicit prompt layers that can be reviewed, versioned, and updated deliberately.
