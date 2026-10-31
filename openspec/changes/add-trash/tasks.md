## 1. Views and URLs

- [x] 1.1 `trash` list view + url (soft-delete models, scoped to active org)
- [x] 1.2 `trashRestore` view + url
- [x] 1.3 `trashDeleteForever` view + url

## 2. Template and navigation

- [x] 2.1 `hub/trash.html` (grouped list, restore / delete-forever with confirm)
- [x] 2.2 Hub tile linking to the trash

## 3. Tests

- [x] 3.1 List shows a deleted object
- [x] 3.2 Restore brings the object back
- [x] 3.3 Permanent delete removes the object
- [x] 3.4 Permissions (403 without `trash.view_all` / `trash.restore_all` / `trash.delete_forever_all`)

## 4. Verify

- [x] 4.1 Full test suite green in Docker
- [x] 4.2 Rebuild Docker for manual testing
