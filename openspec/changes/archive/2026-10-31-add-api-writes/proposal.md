## Why

§7a describes an API-first architecture. The read-only API exists; write
operations are still missing. The simple models (locations, tags, article types,
storage types) have no business logic beyond validation, so they can be exposed
for full CRUD.

## What Changes

- The location, tag, article-type, and storage-type viewsets become full CRUD
  (`ModelViewSet`).
- The `code` and `organisation` fields are read-only in the serializers (they are
  generated / set from the active organisation).
- Delete uses the soft-delete the models already implement.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `api`: write operations for the simple models.

## Impact

- `api/views.py` and `api/serializers.py`.
- **Deferred**: writes for articles, storages, spaces, and occasions (their
  create flows carry business logic that must first move into a shared service).
