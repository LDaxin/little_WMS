# import Specification

## Purpose
TBD - created by archiving change add-article-import. Update Purpose after archive.
## Requirements
### Requirement: Parse a CSV with delimiter and header detection

The system SHALL detect the delimiter (`,` or `;` or tab) and map the header
names (German or English) to the canonical columns `name`, `type`, `menge`,
`storage`, `zustand`. Unknown headers SHALL be ignored.

#### Scenario: Semicolon delimiter

- **WHEN** the file uses `;` as the delimiter
- **THEN** the columns are split correctly

#### Scenario: German headers

- **WHEN** the header is `Name, Typ, Menge, Lagerort, Zustand`
- **THEN** the columns are mapped to name, type, menge, storage, zustand

### Requirement: Preview an import

The system SHALL preview an import without creating anything, classifying rows
as valid, errors, unknown types, unknown storages, and duplicates.

#### Scenario: Preview shows the classification

- **WHEN** the user uploads a file
- **THEN** the counts and the unknown types/storages and duplicates are shown, and nothing is created

#### Scenario: Invalid row

- **WHEN** a row has no name or an invalid quantity
- **THEN** it is listed as an error with its row number and reason

### Requirement: Resolve unknown types and storages

The system SHALL let the user decide, per unknown type and storage, whether to
create it, map it to an existing one, or skip its rows.

#### Scenario: Create a missing type

- **WHEN** the user chooses to create an unknown type
- **THEN** the type is created and its rows are imported

#### Scenario: Map to an existing type

- **WHEN** the user maps an unknown type to an existing one
- **THEN** the rows use that type

#### Scenario: Skip

- **WHEN** the user skips an unknown type
- **THEN** its rows are reported as failed and nothing is created for them

### Requirement: Handle duplicates

The system SHALL let the user choose to skip or update rows whose name and type
already exist.

#### Scenario: Skip duplicates

- **WHEN** the user chooses to skip duplicates
- **THEN** existing articles are left unchanged and the rows are counted as skipped

#### Scenario: Update duplicates

- **WHEN** the user chooses to update duplicates
- **THEN** the existing article's stock and condition are updated

### Requirement: Import report

The system SHALL report how many rows were imported, updated, and skipped, and
for each failed row the row number and the reason.

#### Scenario: Report

- **WHEN** an import finishes
- **THEN** the imported/updated/skipped counts and the failed rows with reasons are shown

### Requirement: Import template

The system SHALL offer a downloadable CSV template with the expected columns and
an example row.

#### Scenario: Download template

- **WHEN** the user downloads the template
- **THEN** a CSV with the header and an example row is returned

### Requirement: Import permission

The system SHALL require the article-create permission to import.

#### Scenario: Permission missing

- **WHEN** a user without `article.create_all` opens the import page
- **THEN** the system responds with 403

