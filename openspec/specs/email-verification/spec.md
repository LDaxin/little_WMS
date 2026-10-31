# email-verification Specification

## Purpose
TBD - created by archiving change add-email-verification. Update Purpose after archive.
## Requirements
### Requirement: Request email verification

The system SHALL create a per-user verification record with a unique token and
SHALL send a confirmation link to the user's address when a user registers or
accepts an invitation as a new user.

#### Scenario: Register

- **WHEN** a user registers
- **THEN** a verification record is created and a confirmation link is sent to their address

#### Scenario: Accept an invitation as a new user

- **WHEN** a new user accepts an invitation
- **THEN** a verification record is created and a confirmation link is sent

#### Scenario: No address

- **WHEN** a user has no email address
- **THEN** no verification record is created and no email is sent

### Requirement: Confirm an email address

The system SHALL mark an address verified when its confirmation link is opened,
and SHALL reject an unknown token.

#### Scenario: Confirm

- **WHEN** a user opens a valid confirmation link
- **THEN** their address is marked verified

#### Scenario: Unknown token

- **WHEN** an unknown confirmation link is opened
- **THEN** the system reports that the link is invalid and verifies nothing

### Requirement: Verification status and resend

The system SHALL show each user's verification status on the users page and
SHALL let an admin resend the confirmation link.

#### Scenario: Show status

- **WHEN** an admin opens the users page
- **THEN** each user's verification status is shown

#### Scenario: Resend

- **WHEN** an admin resends the confirmation for a user
- **THEN** a new token is issued and a confirmation link is sent

