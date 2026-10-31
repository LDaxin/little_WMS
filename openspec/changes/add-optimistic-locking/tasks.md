## 1. Model

- [x] 1.1 `version` on `Article` + `ArticleBase` + migration

## 2. Update flow

- [x] 2.1 The form carries the version
- [x] 2.2 Compare + increment; conflict message

## 3. Tests

- [x] 3.1 Save with the current version increments
- [x] 3.2 Save with a stale version is rejected

## 4. Verify

- [x] 4.1 Full test suite green in Docker
- [x] 4.2 Rebuild Docker for manual testing
