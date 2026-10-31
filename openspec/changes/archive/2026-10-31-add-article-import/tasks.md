## 1. Parsing

- [x] 1.1 `parse_csv` with delimiter detection and header aliases

## 2. Preview

- [x] 2.1 `preview_import` classifies rows (valid, errors, unknown types/storages, duplicates)
- [x] 2.2 Upload view renders the preview with per-item choices

## 3. Import

- [x] 3.1 `import_articles` applies create/map/skip and duplicate skip/update
- [x] 3.2 Confirm view imports and shows the report

## 4. Template & samples

- [x] 4.1 CSV template download
- [x] 4.2 Example CSV files (comma and German semicolon)

## 5. Tests

- [x] 5.1 Delimiter detection and German headers
- [x] 5.2 Preview classification
- [x] 5.3 Create / map / skip unknown type and storage
- [x] 5.4 Duplicate skip and update
- [x] 5.5 Report, template, permission

## 6. Verify

- [x] 6.1 Full test suite green in Docker
- [x] 6.2 Rebuild Docker for manual testing
