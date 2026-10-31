## Why

§27 describes Soft-Delete & Trash. The soft-delete mechanism is already active
everywhere (every model inherits `SoftDeleteObject`), but there is no way to see
or restore deleted objects. A user who deletes an article, storage, or occasion
by mistake loses it from their view forever, even though it still exists in the
database.

## What Changes

- A Trash view listing all soft-deleted objects of the active organisation.
- Restore an object (restores its whole change set).
- Permanently delete an object (with confirmation).
- Guarded by the existing `trash.view_all`, `trash.restore_all`, and
  `trash.delete_forever_all` permissions.

## Capabilities

### New Capabilities

- `trash`: view, restore, and permanently delete soft-deleted objects.

### Modified Capabilities

<!-- none -->

## Impact

- New views/urls/template in the `hub` app (cross-cutting).
- A hub tile linking to the trash.
- No new model or migration (uses the existing soft-delete tables).
- **Deferred**: filtering by "who deleted" (the soft-delete records store no
  user), and filtering by type/date.
