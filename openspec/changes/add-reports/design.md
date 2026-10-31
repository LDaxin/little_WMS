## Context

§33 describes reporting. The dashboard widgets exist; this change adds a reports
view with a few reports, a time-range filter, and CSV export.

## Goals / Non-Goals

**Goals:**

- A `/reports/` view with movements over time, usage, and user activity.
- A time-range filter and CSV export.

**Non-Goals:**

- Diagrams (bar/line); PDF export.
- The Query Builder filter (§9).
- Storage-usage / occasion-history / consumption reports; forecasts.

## Decisions

### Decision 1: A `reports` app

Reporting is a distinct concern; a dedicated app keeps the views and templates
together.

### Decision 2: Reports from the audit log

Movements are `AuditLog` entries with action `moved`/`removed`. The reports
aggregate them by month, by article, and by user.

### Decision 3: A time-range filter

`from`/`to` query parameters (default: the last 12 months) bound every report.

### Decision 4: CSV export

`/reports/export.csv` returns the movements-over-time table as CSV, reusing the
existing CSV pattern.

### Decision 5: Permission

The reports require `settings.view_all`.

## Risks / Trade-offs

- [Aggregation in Python] → fine for a small WMS; can move to the DB later.

## Migration Plan

- None.
