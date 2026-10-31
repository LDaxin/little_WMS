## ADDED Requirements

### Requirement: Optimistic locking

Editable objects SHALL carry a version that is compared on save: a save with a
stale version SHALL be rejected with a conflict message, and a successful save
SHALL increment the version.

#### Scenario: Save with the current version

- **WHEN** a user saves an article with the version they loaded
- **THEN** the change is saved and the version is incremented

#### Scenario: Save with a stale version

- **WHEN** a user saves an article whose version changed since they loaded it
- **THEN** the save is rejected with a conflict message and nothing changes
