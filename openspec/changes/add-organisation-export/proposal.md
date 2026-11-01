## Why

§17 lists backup. Level 1 (full SQLite backup) exists; Level 2 (per-organisation
export/import) is missing. It lets an organisation be moved to another instance
or restored without touching the others.

## What Changes

- Export one organisation's inventory as JSON (article types, storage types,
  locations, tag categories, tags, spaces, storages, article bases, articles,
  stocks, composition items).
- Import such a JSON into a **new** organisation, assigning new primary keys and
  remapping foreign keys.
- A management command and a superuser download/upload on the server settings
  page.

## Capabilities

### New Capabilities

- `organisation-export`: per-organisation JSON export and import.

### Modified Capabilities

<!-- none -->

## Impact

- New `organisation/export.py`, management commands, server-settings actions,
  tests.
- **Deferred**: occasions, loans, movements, audit log; merging into an existing
  organisation.
