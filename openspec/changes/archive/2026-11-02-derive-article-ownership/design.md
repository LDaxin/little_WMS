## Context

`Loan` records both directions (`out` = the organisation lends, `in` = the
organisation borrows) with a status (`pending`/`active`/`returned`). The
`Article.ownership` field was set alongside the loan but never read, so it is
redundant state that can drift.

## Goals / Non-Goals

**Goals:**

- One source of truth for "this article is borrowed in": the open loan.
- No behaviour change for callers that read `ownership`.

**Non-Goals:**

- Query optimisation (the property costs one query per access).
- Changing the loan model or its statuses.

## Decisions

### Decision 1: Derive `ownership` as a property

`Article.ownership` returns `borrowed` when an open loan with direction `in`
exists, else `owned`. The reverse relation uses the loan's manager, so
soft-deleted loans do not count.

### Decision 2: Keep the API field

The article serializer exposes `ownership` as a read-only field, so the API
shape is unchanged even though the value is now derived.

## Risks / Trade-offs

- [N+1] → the property queries per article; the API list does one query per row.
  Acceptable for now; annotate later if it matters. Marked with a `ponytail:`
  comment.

## Migration Plan

- `RemoveField` on `article.article`. The value is derivable from `loans`, so no
  data migration is needed. Rollback: re-add the field with its default.
