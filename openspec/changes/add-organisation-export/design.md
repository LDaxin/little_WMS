## Context

§17 lists backup. Level 1 (full SQLite backup) exists. This change adds Level 2:
a per-organisation JSON export and import.

## Goals / Non-Goals

**Goals:**

- Export one organisation's inventory as JSON.
- Import it into a new organisation, remapping foreign keys.
- A management command and a superuser download/upload.

**Non-Goals:**

- Occasions, loans, movements, audit log.
- Merging into an existing organisation.
- Preserving primary keys or codes.

## Decisions

### Decision 1: A fixed, topological export order

Objects are exported in dependency order (types → locations → tags → spaces →
storages → article bases → articles → stocks → compositions). Foreign keys are
serialised as `{"__ref__": [model, pk]}`.

### Decision 2: Import creates a new organisation

The import always creates a fresh organisation, so it never merges into or
corrupts existing data. Foreign keys are remapped through a `(model, old_pk) →
new object` map; self-references (parent) are resolved in a second pass.

### Decision 3: Codes and primary keys are regenerated

`UuidCode` and the `code` fields are skipped; the models' `save()` creates new
codes. Primary keys are new. This avoids collisions when importing into a
database that already has the original codes.

## Risks / Trade-offs

- [Self-references] → resolved in a second pass.
- [No merge] → importing into an existing organisation is not supported; a new
  one is always created.

## Migration Plan

- None.
