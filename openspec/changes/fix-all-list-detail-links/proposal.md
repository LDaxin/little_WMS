## Why

On the "all" list pages (`/article/`, `/storage/`) the detail link in the shared
result rows is relative (`./<id>`), so it resolves to `/article/<id>` /
`/storage/<id>` — URLs that do not exist (the detail routes need the type:
`/article/<typ>/<id>`, `/storage/<typ>/<id>`). The link is therefore broken on
those pages.

## What Changes

- The result rows build the detail link with the type for articles and storages.
- The "all" list pages show a type column (the type varies there).
- The "all" search views load the type (`select_related`) to avoid a query per
  row.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `article-management`: the all-articles list links to each article's detail page
  and shows its type.
- `storage-management`: the all-storages list links to each storage's detail page
  and shows its type.

## Impact

- `hub` app: `results.html`, `search.html`.
- `article` app: `articlesAll`, `searchArticlesAll`, `searchArticle`.
- `storage` app: `storagesAll`, `searchStoragesAll`, `searchStorages`.
