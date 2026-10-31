# reports Specification

## Purpose
TBD - created by archiving change add-reports. Update Purpose after archive.
## Requirements
### Requirement: Reports view

The system SHALL provide a reports view with a time-range filter showing:
movements over time (per month), usage (the most-moved articles), and user
activity (movements per user). The current selection SHALL be exportable as CSV.

#### Scenario: Movements over time

- **WHEN** a user opens the reports view for a time range
- **THEN** the movements per month in that range are shown

#### Scenario: Usage

- **WHEN** a user opens the reports view
- **THEN** the most-moved articles are shown

#### Scenario: User activity

- **WHEN** a user opens the reports view
- **THEN** the movements per user are shown

#### Scenario: CSV export

- **WHEN** the user exports the current selection
- **THEN** a CSV file is returned

#### Scenario: Permission missing

- **WHEN** a user without `settings.view_all` opens the reports
- **THEN** the system responds with 403

