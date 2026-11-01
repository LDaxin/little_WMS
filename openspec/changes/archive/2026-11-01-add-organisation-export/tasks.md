## 1. Service

- [x] 1.1 `organisation/export.py` `export_organisation(organisation)` → dict
- [x] 1.2 `import_organisation(data, name=None)` → new organisation, remapping FKs

## 2. Commands

- [x] 2.1 `export_organisation <slug> <path>`
- [x] 2.2 `import_organisation <path>`

## 3. UI

- [x] 3.1 Server settings: download export + upload import (superuser)

## 4. Tests

- [x] 4.1 Export contains the organisation's objects only
- [x] 4.2 Import creates a new organisation with the objects
- [x] 4.3 References (including self-references) are remapped
- [x] 4.4 Commands and UI actions

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker and restart the container
