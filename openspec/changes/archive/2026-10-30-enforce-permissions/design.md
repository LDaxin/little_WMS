## Context

`organisation/decorators.py` already has `require_perm(perm)`, used on the
roles/users pages. The catalogue (§3) defines the permissions. This change
applies the decorator to every other view.

## Goals / Non-Goals

**Goals:**

- Every view is guarded by the matching catalogue permission.
- Consistent 403 behaviour; superusers pass.

**Non-Goals:**

- Object-level `assigned` scoping (no assignment field exists yet) — this change
  uses the `_all` scope.
- The dashboard's role-specific widgets (§24).

## Decisions

### Decision 1: Reuse `require_perm`, use the `_all` scope

`require_perm("article.view_all")` etc. The `assigned` scope is not implemented
(no assignment), so `_all` is the effective scope for now.

### Decision 2: Mapping (view → permission)

| Area | View | Permission |
|---|---|---|
| article | list, detail, search, scanner, form fragments | `article.view_all` |
| article | add | `article.create_all` |
| article | update, tags | `article.edit_all` |
| article | delete | `article.delete_all` |
| article | store, remove, store-to-default | `article.move_all` |
| article | export CSV | `export.csv_all` |
| article | composition add/remove/set-global | `storage.edit_all` |
| storage | list, detail, search, scanner, form fragments | `storage.view_all` |
| storage | add | `storage.create_all` |
| storage | update, tags | `storage.edit_all` |
| storage | delete | `storage.delete_all` |
| storage | store/remove contents | `article.move_all` |
| storage | export CSV | `export.csv_all` |
| tag | list, detail, search, form fragments | `tag.view_all` |
| tag | add / update / delete | `tag.create_all` / `tag.edit_all` / `tag.delete_all` |
| location | list, detail, search, form fragments | `location.view_all` |
| location | add / update / delete | `location.create_all` / `location.edit_all` / `location.delete_all` |
| code | list, search, add-modal, resolve link | `code.view_all` |
| code | add | `code.create_all` |
| code | export CSV | `code.export_all` |
| export | QR sheet | `export.qr_sheet_all` |
| movement | page, scan, buffer, store, remove, undo, search, scanner | `article.move_all` |
| movement | "Where is…?" | `article.view_all` |
| inventory | page, scan, search, clear, export | `article.view_all` |

### Decision 3: Public views stay open

`hub` (dashboard), `selectOrganisation`, `switchOrganisation`, and
`inviteAccept` require only authentication (or nothing), because they are the
landing/self-service pages.

## Risks / Trade-offs

- [Locking out users] → the role templates grant the needed `_all` permissions;
  superusers always pass.
- [Many small edits] → mechanical, covered by tests.

## Migration Plan

- No model or migration changes; decorators only.

## Open Questions

- Should `assigned` scoping be implemented next? (separate change)
