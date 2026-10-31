## ADDED Requirements

### Requirement: Borrow via a share link

A share link SHALL carry permissions (default `view`) and a confirmation flag.
When a link allows `borrow`, a logged-in user SHALL be able to borrow the view's
articles, creating a loan that is `pending` when confirmation is required,
otherwise `active`.

#### Scenario: Borrow via a link

- **WHEN** a logged-in user borrows an article from a link that allows borrowing
- **THEN** a loan is created for the user's organisation

#### Scenario: Confirmation

- **WHEN** the link requires confirmation
- **THEN** the loan is pending until confirmed

#### Scenario: No borrow permission

- **WHEN** a link does not allow borrowing
- **THEN** no borrow action is offered

### Requirement: Offers are saved views

Loan offers SHALL be expressed as saved views shared via share links, not as
separate models.

#### Scenario: An offer is a shared view

- **WHEN** an organisation offers articles for loan
- **THEN** it shares a saved view via a share link
