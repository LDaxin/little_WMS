# lend-links Specification

## Purpose
TBD - created by archiving change add-lend-links. Update Purpose after archive.
## Requirements
### Requirement: Create a lend link

The system SHALL let an organisation member create a capability link that an
external person can use to lend items to the organisation. The link SHALL stay
valid until it is deactivated or expires.

#### Scenario: Create a link

- **WHEN** a member creates a lend link
- **THEN** a link with a token is created

### Requirement: Manage lent items via the link

The system SHALL show a public page for a valid lend link where the external
person enters their name and email once, then manages a list of items: adding,
editing (name, description, period) and deleting them. Each item SHALL create a
borrowed article, a loan (direction `in`, party type `person`) and a `loan`
calendar entry.

#### Scenario: Enter the lender details

- **WHEN** the external person opens the link for the first time
- **THEN** they are asked for their name and email

#### Scenario: Add an item

- **WHEN** the external person adds an item
- **THEN** a borrowed article, a loan and a calendar entry are created

#### Scenario: Edit an item

- **WHEN** the external person edits an item's name, description or period
- **THEN** the article and calendar entry are updated

#### Scenario: Delete an item

- **WHEN** the external person deletes an item
- **THEN** the article and loan are removed

#### Scenario: Invalid link

- **WHEN** a lend link is invalid (deactivated or expired)
- **THEN** the page is not shown

### Requirement: Deactivate a lend link

The system SHALL let an organisation member deactivate a lend link. Deactivating
SHALL remove the link's items from the system and anonymise the lender's
personal data.

#### Scenario: Deactivate

- **WHEN** a member deactivates a lend link
- **THEN** the link's items are removed and the lender's name and email are anonymised

