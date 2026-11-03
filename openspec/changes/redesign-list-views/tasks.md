## 1. Column registry

- [x] 1.1 A flat column registry per list type (key, label, level, sortable field, renderer)
- [x] 1.2 Article columns (default + optional)
- [x] 1.3 Storage columns (default + optional)
- [x] 1.4 Renderer types: text, badge (condition), location, quantity, image

## 2. Table rendering from the registry

- [ ] 2.1 The result partial renders header + rows from the registry
- [ ] 2.2 The result partial owns the whole list (header + rows)
- [ ] 2.3 Article list as a grouped stock list (one row per article/location, first row total, collapsible)
- [ ] 2.4 Storage list from the registry

## 3. Sorting

- [ ] 3.1 `sort` URL parameter → `order_by` via the registry
- [ ] 3.2 Sortable header links with direction toggle

## 4. Pagination

- [ ] 4.1 Server-side `?page=N`
- [ ] 4.2 Desktop page numbers (replace)
- [ ] 4.3 Mobile "load more" (append)

## 5. View state

- [ ] 5.1 `sort`/`cols`/`page` in URL parameters
- [ ] 5.2 `SavedView.sort`, `columns`, `display_mode` + apply
- [ ] 5.3 Per-user default column selection

## 6. Cards and view mode

- [ ] 6.1 Card partial (article, storage)
- [ ] 6.2 `X-View-Mode` client hint; `view_mode` wins
- [ ] 6.3 Desktop table/card toggle

## 7. Bulk selection

- [ ] 7.1 Desktop checkbox column
- [ ] 7.2 Mobile selection mode (button + long-press) + action bar
- [ ] 7.3 "Select all" = all matches (server-side)

## 8. Verify

- [ ] 8.1 Tests for registry, sorting, pagination, grouping, cards, selection
- [ ] 8.2 Full suite green in Docker
- [ ] 8.3 Rebuild + restart
