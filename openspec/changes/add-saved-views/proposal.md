## Why

§10 describes saved views: users save a query (from the Query Builder §9) under
a name and reuse it. Today a query is lost as soon as the page is left.

## What Changes

- A `savedviews` app with a `SavedView` model (name, description, owner,
  organisation, the query JSON, shared flag).
- "Save as View" on the article list saves the current query.
- A "My Views" page lists own and shared views; applying one loads its query.

## Capabilities

### New Capabilities

- `saved-views`: saving and reusing query-builder views.

### Modified Capabilities

<!-- none -->

## Impact

- New `savedviews` app; the article list can load a saved view.
- **Deferred**: share links (capability URLs, tokens, access modes, permissions,
  expiry, password); sort / columns / display mode; dashboard custom widgets;
  other list views.
