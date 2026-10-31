## ADDED Requirements

### Requirement: Calendar view

The system SHALL provide a calendar view that lists the calendar entries of the
active organisation, grouped by month, showing each entry's type, title, and
dates. Occasion entries SHALL link to their occasion detail page.

#### Scenario: List calendar entries

- **WHEN** a user with `calendar.view_all` opens the calendar
- **THEN** the calendar entries are listed grouped by month

#### Scenario: An occasion entry links to its occasion

- **WHEN** the calendar shows an occasion entry
- **THEN** it links to the occasion's detail page

#### Scenario: View permission missing

- **WHEN** a user without `calendar.view_all` opens the calendar
- **THEN** the system responds with 403
