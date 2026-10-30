## 1. Article views

- [ ] 1.1 Guard view/list/search/scanner/forms with `article.view_all`
- [ ] 1.2 Guard add with `article.create_all`
- [ ] 1.3 Guard update and tags with `article.edit_all`
- [ ] 1.4 Guard delete with `article.delete_all`
- [ ] 1.5 Guard store/remove/store-to-default with `article.move_all`
- [ ] 1.6 Guard CSV export with `export.csv_all`
- [ ] 1.7 Guard composition views with `storage.edit_all`

## 2. Storage views

- [ ] 2.1 Guard view/list/search/scanner/forms with `storage.view_all`
- [ ] 2.2 Guard add / update / delete with `storage.create_all` / `storage.edit_all` / `storage.delete_all`
- [ ] 2.3 Guard store/remove contents with `article.move_all`
- [ ] 2.4 Guard CSV export with `export.csv_all`

## 3. Tag and location views

- [ ] 3.1 Guard tag views with `tag.*`
- [ ] 3.2 Guard location views with `location.*`

## 4. Code, export, movement

- [ ] 4.1 Guard code views with `code.*` and `code.export_all`
- [ ] 4.2 Guard QR sheet with `export.qr_sheet_all`
- [ ] 4.3 Guard movement (store/remove/undo) with `article.move_all`
- [ ] 4.4 Guard "Where is…?" and inventory with `article.view_all`

## 5. Tests

- [ ] 5.1 Missing permission → 403 on a representative view per area
- [ ] 5.2 Granted permission → 200 on the same views
- [ ] 5.3 Superuser passes

## 6. Verify

- [ ] 6.1 Full test suite green in Docker
- [ ] 6.2 Rebuild Docker for manual testing
