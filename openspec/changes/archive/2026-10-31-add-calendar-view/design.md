## Context

§2 describes the calendar as the central planning view. The `planning` app owns
`CalendarEntry`; this change adds the view.

## Goals / Non-Goals

**Goals:**

- List all calendar entries of the active organisation, grouped by month.
- Link occasion entries to their detail page.

**Non-Goals:**

- The article-level mini calendar.
- Month navigation / filters.
- A month-grid layout.

## Decisions

### Decision 1: A grouped list, not a grid

The calendar is a chronological list grouped by month (a month header plus the
entries). This is the simplest "central planning view" that works; a month grid
can come later.

### Decision 2: Permission

The view requires `calendar.view_all` (already in the §3 catalogue).

### Decision 3: URL

`/calendar/` (the user-facing name from §2), served by the `planning` app.

## Risks / Trade-offs

- [Long list] → fine for a small WMS; navigation/filters are a later change.

## Migration Plan

- None.
