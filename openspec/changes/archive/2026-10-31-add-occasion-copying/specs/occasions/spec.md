## ADDED Requirements

### Requirement: Duplicate an occasion

The system SHALL let a user duplicate an occasion from its detail page. The copy
SHALL have the same occasion type, location, participant count, and packlist.
The dates SHALL be shifted by an optional number of days (default 0).

#### Scenario: Duplicate an occasion

- **WHEN** the user duplicates an occasion
- **THEN** a copy is created with the same type and packlist

#### Scenario: Shift the dates

- **WHEN** the user duplicates an occasion with a shift of N days
- **THEN** the copy's dates are the original dates plus N days

#### Scenario: Duplicate permission missing

- **WHEN** a user without `occasion.create_all` duplicates an occasion
- **THEN** the system responds with 403
