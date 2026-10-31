## ADDED Requirements

### Requirement: Import articles from CSV

The system SHALL import articles from an uploaded CSV with the columns `name`,
`type`, `menge`, `storage`, and `zustand`. `name` and `type` SHALL be required;
`menge` SHALL default to 1, an empty `storage` SHALL mean the not-stored pile,
and `zustand` SHALL default to `gut`.

#### Scenario: Import a valid row

- **WHEN** a row has a name, a known type, and a quantity
- **THEN** an article and its stock are created

#### Scenario: Storage by name

- **WHEN** a row names an existing storage
- **THEN** the stock is placed in that storage's space

#### Scenario: Unknown type

- **WHEN** a row names a type that does not exist
- **THEN** the row is reported as failed and nothing is created for it

#### Scenario: Unknown storage

- **WHEN** a row names a storage that does not exist
- **THEN** the row is reported as failed and nothing is created for it

#### Scenario: Missing name

- **WHEN** a row has no name
- **THEN** the row is reported as failed

### Requirement: Import report

The system SHALL report how many rows were imported and, for each failed row,
the row number and the reason.

#### Scenario: Report

- **WHEN** an import finishes
- **THEN** the number imported and the failed rows with reasons are shown

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
