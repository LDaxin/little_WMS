## Why

§20 has two models for one concept: `Lending` (the organisation lends an article
out) and `Loan` (the organisation borrows one). They duplicate fields, views and
the overdue-notification logic, and only `Lending` uses a `CalendarEntry` — so
only one direction shows in the calendar (RF-001).

## What Changes

- Replace `Lending` and `Loan` with a single `Loan` model carrying a `direction`
  (`out` = lent out, `in` = borrowed in).
- The period of every loan SHALL be a `loan` `CalendarEntry` (both directions).
- One loan list and one return/confirm path; the article-page "Lend" / "Borrow"
  actions create a `Loan` with the matching direction.
- **BREAKING**: remove the `Lending` model and the `/lendings/` page.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `loans`: one `Loan` model with a direction replaces `Loan` + `Lending`; the
  period is a calendar entry for both directions.

## Impact

- `loans/models.py`, `loans/views.py`, `loans/urls.py`, `loans/templates/`.
- `notifications/checks.py`, `savedviews/views.py`, `security/views.py`.
- Migration removes `Lending` and rebuilds `Loan` (0 rows in the dev DB).
- `hub/templates/hub/hub.html` (tile → `/loans/`).
