## Why

§19 lists import. New organisations often have their inventory in a spreadsheet;
without import they would type hundreds of articles by hand. This is the
practical blocker for using the system with real data.

## What Changes

- A CSV import for articles: upload a file with the columns `name`, `type`,
  `menge`, `storage`, `zustand`.
- Validation per row (unknown type/storage, invalid quantity, missing name) with
  a report of imported and failed rows.
- A downloadable CSV template with the expected columns and an example row.

## Capabilities

### New Capabilities

- `import`: CSV import of articles with validation and a report.

### Modified Capabilities

<!-- none -->

## Impact

- New `article/importer.py` service, an import view/template/urls, tests.
- **Deferred**: column-mapping UI, Excel (`openpyxl`), HTMX preview, importing
  storages/locations/tags/types, duplicate handling.
