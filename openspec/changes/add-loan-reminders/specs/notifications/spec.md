## ADDED Requirements

### Requirement: Return-overdue trigger

The system SHALL provide a `return_overdue` trigger that finds active loans
whose return date has passed, in both directions (articles lent out and articles
borrowed in).

#### Scenario: Lent-out loan overdue

- **WHEN** an active lending's loan period has ended
- **THEN** a `return_overdue` finding is produced

#### Scenario: Borrowed-in loan overdue

- **WHEN** an active borrowed-in loan's end date has passed
- **THEN** a `return_overdue` finding is produced

#### Scenario: Returned loan

- **WHEN** a loan has been returned
- **THEN** no finding is produced for it

#### Scenario: No duplicates

- **WHEN** the check runs again while the loan is still overdue
- **THEN** no second notification is created for the same loan
