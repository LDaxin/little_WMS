## ADDED Requirements

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
