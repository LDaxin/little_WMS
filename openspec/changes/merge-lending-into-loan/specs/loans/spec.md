## MODIFIED Requirements

### Requirement: Lend an article to an external person

The system SHALL let a user record a loan of an article to a private person,
with the borrower's name and email, a period, and an optional occasion. The loan
period SHALL be a calendar entry of type `loan`. This is a `Loan` with
`direction` `out`.

#### Scenario: Create a loan

- **WHEN** the user lends an article to a person
- **THEN** a loan and a `loan` calendar entry for the period are created

#### Scenario: The loan appears in the calendar

- **WHEN** a loan exists
- **THEN** its calendar entry is listed in the calendar and the article's mini calendar

### Requirement: Manage loans

The system SHALL list loans of both directions in one list and SHALL let a user
record the return of a loan.

#### Scenario: List loans

- **WHEN** the user opens the loan list
- **THEN** the loans are listed with their party and status, both directions

#### Scenario: Return a loan

- **WHEN** the user records a loan's return
- **THEN** the loan's status becomes returned

#### Scenario: Permission missing

- **WHEN** a user without `article.move_all` creates a loan
- **THEN** the system responds with 403

### Requirement: Borrow an article from an external lender

The system SHALL let a user record that the organisation borrows an article from
an external person or another organisation, with the lender, an optional
occasion, a period, and a status. The period SHALL be a `loan` calendar entry.
This is a `Loan` with `direction` `in`. The borrowed article SHALL be marked as
not owned by the organisation.

#### Scenario: Borrow from a person

- **WHEN** the user records a loan from an external person
- **THEN** a loan and a `loan` calendar entry are created and the article is marked borrowed

#### Scenario: Borrow from an organisation

- **WHEN** the user records a loan from another organisation
- **THEN** the loan records the lending organisation

#### Scenario: Return a borrowed article

- **WHEN** the user records the return
- **THEN** the loan's status becomes returned

#### Scenario: Permission missing

- **WHEN** a user without `article.move_all` records a loan
- **THEN** the system responds with 403

## REMOVED Requirements

### Requirement: Lending out (renamed)

**Reason**: The lending-out direction is merged into the single `Loan` model,
distinguished by `direction = "out"` (RF-001).

**Migration**: Use `Loan` with `direction = "out"`; the article-page "Lend"
action creates it and the `/loans/` list shows it.
