## 1. Column registry

- [x] 1.1 A flat column registry per list type (key, label, level, sortable field, renderer)
- [x] 1.2 Article columns (default + optional)
- [x] 1.3 Storage columns (default + optional)
- [x] 1.4 Renderer types: text, badge (condition), location, quantity, image

## 2. Table rendering from the registry

- [x] 2.1 The result partial renders header + rows from the registry
- [x] 2.2 The result partial owns the whole list (header + rows)
- [x] 2.3 Article list as a grouped stock list (one row per article/location, first row total, collapsible)
- [x] 2.4 Storage list from the registry

## 3. Sorting

- [x] 3.1 `sort` URL parameter → `order_by` via the registry
- [x] 3.2 Sortable header links with direction toggle
- [ ] 3.3 Sort by quantity (stock level) via an annotation

## 4. Pagination

- [x] 4.1 Server-side `?page=N`
- [x] 4.2 Desktop page numbers (replace)
- [x] 4.3 Mobile "load more" (append)

## 5. View state

- [x] 5.1 `sort`/`cols`/`page` in URL parameters
- [x] 5.2 `SavedView.sort`, `columns`, `display_mode` + apply
- [x] 5.3 Per-user default column selection

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

## 9. Scrollable list

- [ ] 9.1 The list has its own scroll area (only the rows scroll)
- [ ] 9.2 Sticky header; aligned with the sidebar and the action bar
