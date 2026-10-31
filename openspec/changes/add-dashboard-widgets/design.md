## Context

§24 describes custom dashboard widgets from saved views. Both exist; this change
connects them.

## Goals / Non-Goals

**Goals:**

- A `show_on_dashboard` flag and the dashboard widgets.

**Non-Goals:**

- Drag-and-drop ordering; per-user show/hide beyond the flag.

## Decisions

### Decision 1: A flag on the saved view

`SavedView.show_on_dashboard` (default off). The dashboard renders the user's own
views with the flag.

### Decision 2: Reuse the query parser

Each widget applies the view's query (via the query builder parser) and lists a
few articles, with a link to apply the view.

## Risks / Trade-offs

- [One query per widget] → fine for a small WMS.

## Migration Plan

- One field on `SavedView`.
