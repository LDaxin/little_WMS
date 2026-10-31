## Context

§10 describes saved views. The Query Builder (§9) produces the query JSON; this
change stores and reuses it.

## Goals / Non-Goals

**Goals:**

- A `SavedView` model storing the query JSON.
- Save from the article list; list own + shared; apply.

**Non-Goals:**

- Share links (capability URLs, tokens, access modes, permissions, expiry,
  password).
- Sort / columns / display mode.
- Dashboard custom widgets; other list views.

## Decisions

### Decision 1: A `savedviews` app

Saved views are a distinct concern; a dedicated app keeps the model and views
together.

### Decision 2: Store the query JSON

`SavedView.query` holds the Query Builder JSON, so applying a view reuses the
existing parser.

### Decision 3: Own + shared

A view is visible to its owner and, when `is_shared`, to the organisation.

### Decision 4: Apply via the article list

The views page links to the article list with `?view=<id>`; the list loads the
view's query into the builder and runs it.

## Risks / Trade-offs

- [Only the article list] → other lists are a later change.

## Migration Plan

- New app with an initial migration.
