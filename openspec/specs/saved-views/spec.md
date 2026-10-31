# saved-views Specification

## Purpose
TBD - created by archiving change add-saved-views. Update Purpose after archive.
## Requirements
### Requirement: Save a view

The system SHALL let a user save the current query under a name, optionally
shared within the organisation.

#### Scenario: Save a view

- **WHEN** the user saves the current query as a view
- **THEN** a saved view with that name and query is created

### Requirement: List and apply saved views

The system SHALL list the user's own and the organisation's shared saved views,
and SHALL let the user apply one to the article list.

#### Scenario: List views

- **WHEN** the user opens the views page
- **THEN** their own and the shared views are listed

#### Scenario: Apply a view

- **WHEN** the user applies a saved view
- **THEN** the article list shows the view's query results

#### Scenario: Delete a view

- **WHEN** the user deletes their own view
- **THEN** it is removed

### Requirement: Create a share link

The system SHALL let a user create a share link for a saved view, with an access
mode (public / guest / internal), an optional expiry, single-use, and an
optional password.

#### Scenario: Create a link

- **WHEN** the user shares a saved view
- **THEN** a share link with a unique token is created

### Requirement: Open a share link

The system SHALL show a share link's saved view read-only, after validating the
token (active, not expired, not used up) and the password when set.

#### Scenario: Open a valid link

- **WHEN** a visitor opens a valid share link
- **THEN** the view's articles are shown read-only

#### Scenario: Expired or revoked link

- **WHEN** a visitor opens an expired or revoked link
- **THEN** the system rejects it

#### Scenario: Single use

- **WHEN** a single-use link is opened once
- **THEN** it can no longer be opened

#### Scenario: Password protected

- **WHEN** a link has a password and the visitor has not entered it
- **THEN** the system asks for the password

### Requirement: Revoke a share link

The system SHALL let a user revoke a share link.

#### Scenario: Revoke

- **WHEN** the user revokes a link
- **THEN** it can no longer be opened

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

