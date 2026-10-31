# gdpr Specification

## Purpose
TBD - created by archiving change add-gdpr. Update Purpose after archive.
## Requirements
### Requirement: Export my data

The system SHALL let a user export their personal data as JSON: their profile,
their activities, and their loans.

#### Scenario: Export

- **WHEN** the user requests their data
- **THEN** a JSON file with their profile, activities, and loans is returned

### Requirement: Delete a user with anonymisation

The system SHALL let an admin delete a user, removing the account and profile
and anonymising the user's audit-log entries (the personal reference is removed,
the log stays).

#### Scenario: Delete a user

- **WHEN** an admin deletes a user
- **THEN** the account is removed and the user's audit-log entries are anonymised

#### Scenario: Permission missing

- **WHEN** a user without the delete permission deletes a user
- **THEN** the system responds with 403

