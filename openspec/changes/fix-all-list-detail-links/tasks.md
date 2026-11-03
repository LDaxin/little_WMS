## 1. Templates

- [x] 1.1 `results.html`: detail link with the type for article/storage
- [x] 1.2 `results.html`: type column when `show_type`
- [x] 1.3 `search.html`: type header column when `show_type`

## 2. Views

- [x] 2.1 `articlesAll` / `storagesAll` pass `show_type`
- [x] 2.2 `searchArticlesAll` / `searchStoragesAll` pass `show_type` + `select_related`
- [x] 2.3 `searchArticle` / `searchStorages` `select_related` the type

## 3. Tests

- [x] 3.1 All-articles search returns the typed detail link
- [x] 3.2 All-storages search returns the typed detail link

## 4. Register

- [x] 4.1 KI-026 in `docs/Known Issues.md`

## 5. Verify

- [x] 5.1 Full suite green in Docker
- [x] 5.2 Rebuild + restart
