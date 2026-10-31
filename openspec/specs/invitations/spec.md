# invitations Specification

## Purpose
TBD - created by archiving change add-invitations. Update Purpose after archive.
## Requirements
### Requirement: Create an invitation

The system SHALL let a user with the invite permission create an invitation for
their organisation, with a role, an expiry (default 7 days), and an optional
email, and SHALL generate a unique token.

#### Scenario: Create a link invitation

- **WHEN** an admin creates an invitation with a role
- **THEN** an invitation with a unique token and a default 7-day expiry is created

#### Scenario: Custom expiry

- **WHEN** the admin sets an expiry
- **THEN** the invitation expires at that time

#### Scenario: Optional email

- **WHEN** the admin provides an email
- **THEN** the invitation is associated with that email (for sending)

### Requirement: Accept an invitation

The system SHALL let a visitor accept a valid invitation by opening its link,
registering or logging in, and SHALL create a membership with the invited role.

#### Scenario: Accept as a new user

- **WHEN** a visitor opens a valid invitation link and registers
- **THEN** a membership in the inviting organisation with the invited role is created

#### Scenario: Accept as an existing user

- **WHEN** a logged-in user opens a valid invitation link
- **THEN** a membership in the inviting organisation with the invited role is created

#### Scenario: Already a member

- **WHEN** the user is already a member of the organisation
- **THEN** the invitation is accepted without creating a duplicate membership

### Requirement: Invitation lifecycle

The system SHALL track an invitation's status and SHALL reject an invitation
that is expired, already accepted, or revoked.

#### Scenario: Expired invitation

- **WHEN** a visitor opens an invitation whose expiry has passed
- **THEN** the system rejects it and shows that it has expired

#### Scenario: Accepted invitation

- **WHEN** a visitor opens an invitation that was already accepted
- **THEN** the system rejects it

### Requirement: Revoke an invitation

The system SHALL let an admin revoke a pending invitation.

#### Scenario: Revoke

- **WHEN** an admin revokes a pending invitation
- **THEN** the invitation can no longer be accepted

### Requirement: Send an invitation email

The system SHALL send the invitation link by email when an invitation is created
with an email address. When email is not configured the invitation is still
created and its link stays available in the UI.

#### Scenario: Invitation with email

- **WHEN** an admin creates an invitation with an email address
- **THEN** the invite link is sent to that address

#### Scenario: Invitation without email

- **WHEN** an admin creates an invitation without an email address
- **THEN** no email is sent and the link is shown in the UI

#### Scenario: Email not configured

- **WHEN** an admin creates an invitation with an email while email is not configured
- **THEN** the invitation is created, no email is sent, and the link stays available

