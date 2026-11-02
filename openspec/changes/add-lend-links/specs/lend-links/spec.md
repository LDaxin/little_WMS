## ADDED Requirements

### Requirement: Create a lend link

The system SHALL let an organisation member create a capability link that an
external person can use to lend an item to the organisation. The link SHALL be
revocable and MAY expire.

#### Scenario: Create a link

- **WHEN** a member creates a lend link
- **THEN** a link with a token is created

#### Scenario: Revoke a link

- **WHEN** a member revokes a lend link
- **THEN** the link is no longer valid

### Requirement: Lend an item via the link

The system SHALL show a public form for a valid lend link where an external
person enters the item name, a description, a period, and an optional photo.
Submitting SHALL create a borrowed article, a loan (direction `in`, party type
`person`) and a `loan` calendar entry.

#### Scenario: Submit the form

- **WHEN** an external person submits the lend form
- **THEN** a borrowed article, a loan and a calendar entry are created

#### Scenario: Invalid link

- **WHEN** a lend link is invalid (revoked or expired)
- **THEN** the form is not shown

### Requirement: See the loan status

The system SHALL show the external person the status of the loan they created
through the link.

#### Scenario: Status after lending

- **WHEN** the external person opens the link after lending
- **THEN** the loan's status is shown
