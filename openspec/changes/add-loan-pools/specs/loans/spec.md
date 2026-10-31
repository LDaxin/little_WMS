## ADDED Requirements

### Requirement: Loan offers

The system SHALL let an organisation create a loan offer (a named list of
articles) with a default confirmation flag, and per-item overrides. Borrowing
from an offer SHALL create a loan that is `pending` when confirmation is
required (resolved item → offer → article), otherwise `active`.

#### Scenario: Create an offer

- **WHEN** the user creates a loan offer with articles
- **THEN** the offer and its items are created

#### Scenario: Borrow with confirmation

- **WHEN** a borrower takes an article from an offer that requires confirmation
- **THEN** a pending loan is created

#### Scenario: Borrow without confirmation

- **WHEN** a borrower takes an article from an offer that does not require confirmation
- **THEN** an active loan is created

#### Scenario: Confirm a pending loan

- **WHEN** the lender confirms a pending loan
- **THEN** the loan becomes active

### Requirement: Shared pools

The system SHALL let an organisation be a member of a pool (another
organisation), with `can_borrow` and `can_add` flags.

#### Scenario: A pool membership

- **WHEN** an organisation is added as a member of a pool
- **THEN** the membership records whether it may borrow and add
