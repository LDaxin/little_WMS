---
name: little-wms-bugfix
description: Use when fixing a bug, recording a defect, or working through docs/Known Issues.md in little_WMS. Covers reproducing, root-cause fixing, regression tests, and keeping the Known Issues register up to date.
---

# little_WMS Bugfix

Workflow for defects in little_WMS. Conventions (branch naming, commit types,
ponytail, merge rules) come from the `little-wms-implementation` skill — this
skill only adds the bug-specific parts.

## Register

`docs/Known Issues.md` is the central register. Every defect lives there as an
entry: ID, location, symptom, status, found-in step, pinned test.

## Recording a finding

When you spot a defect (during characterization, review, or normal work):

1. Add an entry to `docs/Known Issues.md` with the next free `KI-xxx` ID.
2. Describe the **current** behaviour, not the desired one.
3. If you can, pin it with a characterization test and fill the *Test* column.
4. Do not fix it in the same step unless asked — recording and fixing are
   separate, reviewable units.

## Fixing a bug

1. **Reproduce** — write a failing test first, or point at the existing
   characterization test that pins the bug.
2. **Root cause, not symptom** — grep every caller of the function you are
   about to touch. Fix it once, where all callers route through. A guard in
   the shared function beats a guard in every caller.
3. **Regression test** — leave one runnable check behind that fails if the bug
   returns.
4. **Update the register** — set the entry's status to ✅ and adjust the pinned
   test if its expectation changed.
5. **Report** — what was broken, the root cause, the fix, the test.

## Rules

- Never simplify away input validation at trust boundaries, error handling
  that prevents data loss, or security checks — those are often the bug.
- Keep the fix minimal; no drive-by refactoring in a bugfix step.
- One bug (or one coherent group) per branch and commit.
