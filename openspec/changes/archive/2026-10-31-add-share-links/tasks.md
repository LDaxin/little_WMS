## 1. Model

- [x] 1.1 `ShareLink` model + migration

## 2. Views and URLs

- [x] 2.1 Create a share link (from a saved view)
- [x] 2.2 Public view `/s/<token>/` (validate, password, read-only)
- [x] 2.3 Revoke

## 3. UI

- [x] 3.1 Share form + link display
- [x] 3.2 Active links overview

## 4. Tests

- [x] 4.1 Create a link
- [x] 4.2 Open a valid link shows the articles
- [x] 4.3 Expired / revoked / single-use rejected
- [x] 4.4 Password required
- [x] 4.5 Revoke

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker for manual testing
