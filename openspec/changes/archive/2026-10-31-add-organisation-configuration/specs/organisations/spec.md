## ADDED Requirements

### Requirement: Organisation configuration

The system SHALL provide a configuration page for the organisation admin that
lists and creates article types and storage types, and SHALL let the admin load
the standard types from §8 and create the standard role templates.

#### Scenario: Create an article type

- **WHEN** the admin adds an article type
- **THEN** it is available when creating articles

#### Scenario: Create a storage type

- **WHEN** the admin adds a storage type
- **THEN** it is available when creating storages

#### Scenario: Load defaults

- **WHEN** the admin loads the defaults
- **THEN** the standard article types and storage types from §8 are created

#### Scenario: Create role templates

- **WHEN** the admin creates the role templates
- **THEN** the standard role templates exist for the organisation

#### Scenario: Permission missing

- **WHEN** a user without `settings.edit_all` opens the configuration page
- **THEN** the system responds with 403
