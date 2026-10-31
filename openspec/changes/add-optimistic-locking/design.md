## Context

§36 describes concurrency. Movements are last-write-wins; edits need optimistic
locking.

## Goals / Non-Goals

**Goals:**

- A `version` on `Article` / `ArticleBase` and the conflict check on update.

**Non-Goals:**

- A version on every model; automatic merging.

## Decisions

### Decision 1: A `version` field

`version` (IntegerField, default 0) on `Article` and `ArticleBase`.

### Decision 2: The form carries the version

The update form includes the loaded version; the view compares it before saving
and increments on success. A mismatch returns a conflict toast.

## Risks / Trade-offs

- [Only the article edit flow] → the main edit path; other models are a later
  change.

## Migration Plan

- One field on `Article` and `ArticleBase`.
