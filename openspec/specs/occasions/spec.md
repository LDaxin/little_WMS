# occasions Specification

## Purpose
TBD - created by archiving change add-occasions. Update Purpose after archive.
## Requirements
### Requirement: Occasion types

The system SHALL let a user define occasion types (e.g. "Summer camp",
"Trip"), each with an optional symbol and custom fields, mirroring article types.

#### Scenario: Create an occasion type

- **WHEN** a user adds an occasion type
- **THEN** it is available when creating occasions

### Requirement: Manage occasions

The system SHALL let a user create, list, edit, and delete occasions with a name,
a type, a date range, an optional location, an optional responsible user, and a
participant count. An occasion SHALL be backed by a calendar entry.

#### Scenario: Create an occasion

- **WHEN** the user creates an occasion
- **THEN** the occasion and its calendar entry are created

#### Scenario: List occasions

- **WHEN** the user opens the occasion list
- **THEN** the occasions are listed

#### Scenario: Delete an occasion

- **WHEN** the user deletes an occasion
- **THEN** the occasion and its calendar entry are removed

### Requirement: Packlist

The system SHALL let the user add and remove articles on an occasion's packlist,
each with a quantity and a status (needed, reserved, checked out, returned).

#### Scenario: Add an article

- **WHEN** the user adds an article with a quantity to the packlist
- **THEN** the article appears on the packlist with that quantity and status "needed"

#### Scenario: Change status

- **WHEN** the user changes a packlist entry's status
- **THEN** the entry's status is updated

#### Scenario: Remove an entry

- **WHEN** the user removes a packlist entry
- **THEN** the article is no longer on the packlist

### Requirement: Occasion permissions

The system SHALL guard the occasion views with the catalogue permissions:
`occasion.view_all`, `occasion.create_all`, `occasion.edit_all`,
`occasion.delete_all`, and `occasion.manage_packlist_all`.

#### Scenario: View permission missing

- **WHEN** a user without `occasion.view_all` opens the occasion list
- **THEN** the system responds with 403

#### Scenario: Packlist permission

- **WHEN** a user without `occasion.manage_packlist_all` edits a packlist
- **THEN** the system responds with 403

