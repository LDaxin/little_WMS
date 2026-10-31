## Context

§7a describes an API-first architecture. The read-only API exists; this change
adds writes for the simple models.

## Goals / Non-Goals

**Goals:**

- Full CRUD for locations, tags, article types, storage types.
- `code` / `organisation` read-only.

**Non-Goals:**

- Writes for articles, storages, spaces, occasions (their create flows carry
  business logic that must first move into a shared service).

## Decisions

### Decision 1: `ModelViewSet` for the simple models

These models have no business logic beyond validation, so DRF's default CRUD is
enough. The complex models stay read-only.

### Decision 2: `code` / `organisation` read-only

`code` is generated in `save()`; `organisation` comes from the active
organisation. Both are marked read-only so clients cannot set them.

### Decision 3: Soft delete

DRF's `perform_destroy` calls `instance.delete()`, which the soft-delete models
implement as a soft delete.

## Risks / Trade-offs

- [No writes for articles yet] → intentional; the article create flow needs a
  service first.

## Migration Plan

- None.
