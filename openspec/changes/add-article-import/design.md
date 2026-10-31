## Context

§19 lists import. The article model is `ArticleBase` (name + type) → `Article`
(identity) → `Stock` (quantity at a `Space`). This change adds a minimal CSV
import for articles.

## Goals / Non-Goals

**Goals:**

- Import articles from a CSV with fixed columns.
- Validate each row and report imported / failed rows with reasons.
- A downloadable template.

**Non-Goals:**

- Column-mapping UI, Excel, HTMX preview.
- Importing storages, locations, tags, types.
- Duplicate-code handling.

## Decisions

### Decision 1: Fixed columns, no mapping UI

The CSV has a header row with `name`, `type`, `menge`, `storage`, `zustand`.
`name` and `type` are required; `menge` defaults to 1, `storage` empty means the
"not stored" pile, `zustand` defaults to `gut`. This avoids the mapping UI while
covering the common case.

### Decision 2: Validate before creating

Each row is validated first; only valid rows create records, so a bad row never
leaves a half-created article. Unknown types/storages are errors (no implicit
creation).

### Decision 3: A service function

`article/importer.py` `import_articles(file, organisation)` returns
`{"imported": n, "errors": [(row, reason)]}` and is called by the view, so it is
testable without HTTP.

## Risks / Trade-offs

- [Fixed columns] → a file with different headers fails clearly; the mapping UI
  is a later change.
- [No transaction per row] → a mid-file failure keeps earlier rows; acceptable
  for an import with a report.

## Migration Plan

- None.
