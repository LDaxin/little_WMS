## ADDED Requirements

### Requirement: Only verified recipients

The central mail service SHALL skip a recipient whose address is not verified,
unless the message is explicitly exempt. It SHALL log the skip and not raise.

#### Scenario: Unverified recipient

- **WHEN** code sends a non-exempt message to an unverified address
- **THEN** the message is skipped and a warning is logged

#### Scenario: Verified recipient

- **WHEN** code sends a non-exempt message to a verified address
- **THEN** the message is sent

#### Scenario: Exempt message

- **WHEN** code sends an exempt message (e.g. an invitation) to an unverified address
- **THEN** the message is sent
