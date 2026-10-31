## Why

§19 lists import. New organisations often have their inventory in a spreadsheet;
without import they would type hundreds of articles by hand. A first CSV import
exists, but it fails a row on an unknown type/storage and does not handle the
German Excel export (semicolon delimiter, German headers).

## What Changes

- A two-step import: upload → **preview** (dry-run) → confirm.
- The preview classifies rows (valid, errors, unknown types, unknown storages,
  duplicates) and lets the user decide per unknown type/storage: create, map to
  an existing one, or skip; and for duplicates: skip or update.
- Delimiter detection (`,` / `;` / tab) so German Excel exports work.
- Header aliases (German and English) mapped to the canonical columns.
- A downloadable CSV template.

## Capabilities

### New Capabilities

- `import`: CSV import of articles with a preview, decisions, validation, and a
  report.

### Modified Capabilities

<!-- none -->

## Impact

- `article/importer.py` (parse, preview, import), import views/templates/urls,
  tests, example CSVs.
- **Deferred**: Excel (`openpyxl`), importing storages/locations/tags/types,
  per-row column mapping UI.
