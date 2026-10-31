## Context

§27 describes Soft-Delete & Trash. The soft-delete mechanism (`SoftDeleteObject`,
`SoftDeleteManager`, `ChangeSet`, `SoftDeleteRecord`) is already in use across
all models; only the trash UI is missing.

## Goals / Non-Goals

**Goals:**

- List soft-deleted objects of the active organisation.
- Restore an object (whole change set).
- Permanently delete an object.

**Non-Goals:**

- Filtering by "who deleted" (the soft-delete records store no user).
- Filtering by type/date.
- Restoring a single object without its change set.

## Decisions

### Decision 1: Discover soft-delete models automatically

The trash iterates `apps.get_models()` and keeps those that subclass
`SoftDeleteObject`, querying each with `objects.deleted_set()`. This avoids a
hardcoded model list that would drift as models are added.

### Decision 2: Scope to the active organisation

`deleted_set()` uses the unfiltered base queryset, so the view filters each
model's deleted objects by `organisation` when the model has that field.

### Decision 3: Restore and permanent delete via the soft-delete API

- Restore: `obj.undelete()` — restores the object and its whole change set.
- Permanent delete: `obj.delete()` — on an already soft-deleted object this
  hard-deletes it and cleans up its change set.

### Decision 4: Permissions

`trash.view_all` for the list, `trash.restore_all` for restore,
`trash.delete_forever_all` for permanent delete — all already in the §3
catalogue.

### Decision 5: Location

The views live in the `hub` app (cross-cutting, like the dashboard) with a hub
tile linking to the trash.

## Risks / Trade-offs

- [N queries] → one query per soft-delete model; fine for a small WMS.
- [Stale records] → a record whose object is gone is skipped.

## Migration Plan

- None (no model change).

## Open Questions

- Should the trash be per-model tabs? (plain grouped list for now)
