## Why

The catalogue has an `assigned` scope, but only `_all` is enforced today. There
is no way to grant someone rights over *only the objects assigned to them* —
e.g. a helper who may move their own articles but not the whole warehouse.

## What Changes

- Articles can be assigned to users (`Article.assigned_to`, M2M).
- A scope-aware check: `_all` grants an action outright; `_assigned` grants it
  only for objects assigned to the user.
- Article views use the scope check; list/search/export filter to assigned
  articles for users who only have the `_assigned` scope; detail/edit/delete/move
  verify the specific article is assigned.
- Article detail gets an "assigned to" editor.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `article-management`: articles can be assigned to users.
- `roles-permissions`: the `assigned` scope is enforced for articles.

## Impact

- `Article` model + migration (`assigned_to`).
- `organisation/permissions.py` + `decorators.py`: scope helpers/decorator.
- `article/views.py`: scope-aware guards and filtering; detail UI.
- Enforcement is extended for **articles only**; storage/occasion follow later.
