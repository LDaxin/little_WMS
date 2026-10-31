## Context

The dashboard links to `/article/` and `/storage/`, which do not exist. This
change adds the all-types list views.

## Goals / Non-Goals

**Goals:**

- `/article/` and `/storage/` listing all objects across types.

**Non-Goals:**

- New UI patterns; the per-type views stay.

## Decisions

### Decision 1: Reuse the existing list structure

The views render the existing `items.html` (with `type` = article/storage and no
type filter); the search endpoints mirror the per-type ones without the type
filter.

### Decision 2: URL order

`/article/search` and `/storage/search` are registered before the per-type
patterns so they are not captured as a type.

## Risks / Trade-offs

- [No add/del/export/qr on the all view] → those need a type; the per-type views
  keep them.

## Migration Plan

- None.
