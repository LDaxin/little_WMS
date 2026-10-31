# loans Specification

## Purpose
TBD - created by archiving change add-loans. Update Purpose after archive.
## Requirements
### Requirement: Lend an article to an external person

The system SHALL let a user record a loan of an article to a private person,
with the borrower's name and email, a period, and an optional occasion. The loan
period SHALL be a calendar entry of type `loan`.

#### Scenario: Create a loan

- **WHEN** the user lends an article to a person
- **THEN** a loan and a `loan` calendar entry for the period are created

#### Scenario: The loan appears in the calendar

- **WHEN** a loan exists
- **THEN** its calendar entry is listed in the calendar and the article's mini calendar

### Requirement: Manage loans

The system SHALL list loans and SHALL let a user record the return of a loan.

#### Scenario: List loans

- **WHEN** the user opens the loan list
- **THEN** the loans are listed with their borrower and status

#### Scenario: Return a loan

- **WHEN** the user records a loan's return
- **THEN** the loan's status becomes returned

#### Scenario: Permission missing

- **WHEN** a user without `article.move_all` creates a loan
- **THEN** the system responds with 403

