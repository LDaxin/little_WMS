## Context

§24 describes the dashboard as the command center. The hub is a tile grid; this
change adds a dashboard page with widgets, reusing the notifications and the
checks layer.

## Goals / Non-Goals

**Goals:**

- A dashboard page with permission-gated widgets.
- Reuse the checks layer for the alerts widget.

**Non-Goals:**

- Custom widgets from Saved Views (§10).
- Per-user show/hide and drag-and-drop ordering.

## Decisions

### Decision 1: A separate page, linked from the hub

The dashboard is `/dashboard/`, linked from the hub, so the tile grid stays the
navigation and the dashboard is the "what matters now" view.

### Decision 2: Widgets gated in the view

The view computes a widget's data only when the user holds its permission, so
the template simply renders what is present. A `has_perm` template filter is
added for future template-level gating.

### Decision 3: Alerts reuse the checks layer

The alerts widget calls `notifications.checks.run_checks`, so the dashboard and
the notification triggers share one source.

## Risks / Trade-offs

- [Several queries per dashboard load] → fine for a small WMS.

## Migration Plan

- None.
