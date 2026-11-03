## Context

`hub/modules/results.html` renders the rows for every list page. The detail link
is `./{{ r.id }}`, relative to the current page. On a type-specific page
(`/article/<typ>/`) that resolves correctly; on the "all" page (`/article/`) it
resolves to `/article/<id>`, which no route matches. Articles and storages are
the only lists whose detail URL carries the type, so only they are affected.

## Goals / Non-Goals

**Goals:**

- The detail link works on the "all" pages.
- The type is visible on the "all" pages (it varies there).

**Non-Goals:**

- Changing the type-specific pages (the type column is redundant there).
- Location, tag and code lists (their detail URLs have no type).

## Decisions

### Decision 1: Build the link with the type

For articles the link is `/article/{{ r.base.pType.name }}/{{ r.id }}`, for
storages `/storage/{{ r.typ.name }}/{{ r.id }}`. This is correct on both the
"all" and the type-specific pages, so one link serves both.

### Decision 2: A `show_type` flag

The "all" views pass `show_type=True`; the type-specific views do not. The flag
gates the extra column in both the header (`search.html`) and the rows
(`results.html`).

### Decision 3: `select_related` the type

The link and the column read the type, so the "all" search views select it to
avoid a query per row.

## Risks / Trade-offs

- [Column alignment] → the header and the rows both gate on `show_type`, so they
  stay aligned.

## Migration Plan

- No schema change.
