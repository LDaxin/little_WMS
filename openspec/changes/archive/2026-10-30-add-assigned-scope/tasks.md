## 1. Model

- [x] 1.1 Add `Article.assigned_to` (M2M to `auth.User`)
- [x] 1.2 Add the migration

## 2. Scope helpers

- [x] 2.1 Add `has_scope` and `is_assigned_only` to `organisation/permissions.py`
- [x] 2.2 Add a `require_scope` decorator in `organisation/decorators.py`

## 3. Article views

- [x] 3.1 Switch article guards to `require_scope("article", …)`
- [x] 3.2 Filter list/search/export for `_assigned`-only users
- [x] 3.3 Re-check the fetched article in detail/update/delete/move (403 if unassigned)

## 4. Assignment UI

- [x] 4.1 "Assigned to" add/remove on the article detail
- [x] 4.2 Views + URLs for assign/unassign

## 5. Tests

- [x] 5.1 `_all` sees everything; `_assigned` sees only assigned
- [x] 5.2 `_assigned` on an unassigned object → 403
- [x] 5.3 `_assigned` on an assigned object works (view/edit/move)
- [x] 5.4 Assign/unassign updates the assignees

## 6. Verify

- [x] 6.1 Full test suite green in Docker
- [x] 6.2 Rebuild Docker for manual testing
