## 1. Model

- [ ] 1.1 Add `Article.assigned_to` (M2M to `auth.User`)
- [ ] 1.2 Add the migration

## 2. Scope helpers

- [ ] 2.1 Add `has_scope` and `is_assigned_only` to `organisation/permissions.py`
- [ ] 2.2 Add a `require_scope` decorator in `organisation/decorators.py`

## 3. Article views

- [ ] 3.1 Switch article guards to `require_scope("article", …)`
- [ ] 3.2 Filter list/search/export for `_assigned`-only users
- [ ] 3.3 Re-check the fetched article in detail/update/delete/move (403 if unassigned)

## 4. Assignment UI

- [ ] 4.1 "Assigned to" add/remove on the article detail
- [ ] 4.2 Views + URLs for assign/unassign

## 5. Tests

- [ ] 5.1 `_all` sees everything; `_assigned` sees only assigned
- [ ] 5.2 `_assigned` on an unassigned object → 403
- [ ] 5.3 `_assigned` on an assigned object works (view/edit/move)
- [ ] 5.4 Assign/unassign updates the assignees

## 6. Verify

- [ ] 6.1 Full test suite green in Docker
- [ ] 6.2 Rebuild Docker for manual testing
