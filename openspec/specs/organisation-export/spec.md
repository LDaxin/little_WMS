# organisation-export Specification

## Purpose
TBD - created by archiving change add-organisation-export. Update Purpose after archive.
## Requirements
### Requirement: Export an organisation

The system SHALL export one organisation's inventory (article types, storage
types, locations, tag categories, tags, spaces, storages, article bases,
articles, stocks, composition items) as JSON, with foreign keys as references.

#### Scenario: Export

- **WHEN** an organisation is exported
- **THEN** a JSON document with its objects and their references is produced

#### Scenario: Only that organisation

- **WHEN** an organisation is exported
- **THEN** only its objects are included

### Requirement: Import an organisation

The system SHALL import such a JSON into a new organisation, assigning new
primary keys and remapping foreign keys.

#### Scenario: Import creates a new organisation

- **WHEN** a JSON is imported
- **THEN** a new organisation with the exported objects is created

#### Scenario: References are remapped

- **WHEN** an object references another exported object
- **THEN** the reference points to the newly created object

#### Scenario: Self-references

- **WHEN** an object references another object of the same model (e.g. a parent)
- **THEN** the reference is resolved

### Requirement: Export and import commands

The system SHALL provide `export_organisation` and `import_organisation`
management commands.

#### Scenario: Export command

- **WHEN** `export_organisation` is run with an organisation and a path
- **THEN** the JSON is written to that path

#### Scenario: Import command

- **WHEN** `import_organisation` is run with a path
- **THEN** a new organisation is created from the JSON

### Requirement: Export and import in the UI

The system SHALL let a superuser download an export and upload an import on the
server settings page.

#### Scenario: Download

- **WHEN** a superuser downloads the export
- **THEN** the JSON is returned as a download

#### Scenario: Upload

- **WHEN** a superuser uploads a JSON
- **THEN** a new organisation is created and reported

#### Scenario: Permission missing

- **WHEN** a non-superuser triggers export or import
- **THEN** the system responds with 403

