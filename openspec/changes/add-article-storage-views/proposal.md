## Why

The dashboard's quick actions link to `/article/` and `/storage/`, but only the
per-type views exist (`/article/<typ>/`). Those links 404.

## What Changes

- `/article/` lists all articles across types (with search + query builder).
- `/storage/` lists all storages across types.
- Matching `/article/search` and `/storage/search` endpoints.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `article-management`: an all-articles list view.
- `storage-management`: an all-storages list view.

## Impact

- New views/urls in the `article` and `storage` apps, reusing the existing
  `items.html` / `search.html` / `results.html` structure.
