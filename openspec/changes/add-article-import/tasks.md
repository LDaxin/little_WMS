## 1. Service

- [x] 1.1 `article/import.py` `import_articles(file, organisation)` with validation + report

## 2. UI

- [x] 2.1 `/import/` upload page (perm `article.create_all`) + report
- [x] 2.2 `/import/template/` CSV template download

## 3. Tests

- [x] 3.1 Valid row creates article + stock
- [x] 3.2 Storage by name places the stock
- [x] 3.3 Unknown type / storage / missing name reported, nothing created
- [x] 3.4 Template download
- [x] 3.5 Permission required

## 4. Verify

- [x] 4.1 Full test suite green in Docker
- [x] 4.2 Rebuild Docker for manual testing
