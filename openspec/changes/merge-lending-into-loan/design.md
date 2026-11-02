## Context

Two models exist for §20: `Lending` (lends out, uses a `CalendarEntry`) and
`Loan` (borrows in, inline dates). `notifications/checks.py` builds near-identical
overdue findings for both (RF-001).

## Goals / Non-Goals

**Goals:**

- One `Loan` model with a `direction`.
- One list, one return/confirm path, one overdue check.
- Every loan period is a `loan` calendar entry.

**Non-Goals:**

- Resolving `Article.ownership` against the open loan (RF-004).
- A pool-management UI.

## Decisions

### Decision 1: `direction` field, not two models

`Loan.direction` is `"out"` (the organisation lends) or `"in"` (the organisation
borrows). Fields: `article`, `calendar_entry`, `party_type`, `party_name`,
`party_email`, `party_organisation`, `occasion`, `status`, `notes`.

### Decision 2: The period is always a CalendarEntry

Both directions create a `loan` `CalendarEntry`; the loan holds the OneToOne.
This folds the lend-out behaviour onto the borrow-in one so both directions
appear in the calendar / mini calendar (§20). `start_date`/`end_date` leave the
model.

### Decision 3: One list page

`/loans/` lists both directions with a direction badge. `/lendings/` is removed;
the hub tile points at `/loans/`. The article-page "Lend" / "Borrow" actions stay
(two entry points, one model).

## Risks / Trade-offs

- [Share-link flow] → creates a `Loan` per borrowed article; it now also creates
  a calendar entry per loan. Acceptable (one entry per borrowed article).
- [No data migration] → the dev DB has 0 loan rows; `ki` is not live.

## Migration Plan

- Remove `Lending`; rebuild `Loan` with the new fields.
- Rollback: reverse the migration (drops the new fields, recreates `Lending`).
