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

### Requirement: Borrow an article from an external lender

The system SHALL let a user record that the organisation borrows an article from
an external person or another organisation, with the lender, an optional
occasion, a period, and a status. The borrowed article SHALL be marked as not
owned by the organisation.

#### Scenario: Borrow from a person

- **WHEN** the user records a loan from an external person
- **THEN** a loan is created and the article is marked borrowed

#### Scenario: Borrow from an organisation

- **WHEN** the user records a loan from another organisation
- **THEN** the loan records the lending organisation

#### Scenario: Return a borrowed article

- **WHEN** the user records the return
- **THEN** the loan's status becomes returned

#### Scenario: Permission missing

- **WHEN** a user without `article.move_all` records a loan
- **THEN** the system responds with 403

### Requirement: Lending out (renamed)

The system SHALL keep the lending-out direction (the organisation lends an
article to an external person) under the name `Lending`.

#### Scenario: Lend out

- **WHEN** the user lends an article to a person
- **THEN** a lending is created

### Requirement: Shared pools

The system SHALL let an organisation be a member of a pool (another
organisation), with `can_borrow` and `can_add` flags, so pool members can borrow
from the pool.

#### Scenario: A pool membership

- **WHEN** an organisation is added as a member of a pool
- **THEN** the membership records whether it may borrow and add

### Requirement: Pending loans

The system SHALL allow a loan to be `pending` until the lender confirms it, used
when borrowing requires confirmation.

#### Scenario: Pending then confirmed

- **WHEN** a loan requires confirmation
- **THEN** it is created pending and becomes active once confirmed

