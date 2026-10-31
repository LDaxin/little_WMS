## ADDED Requirements

### Requirement: Invitation link after approval

When a server admin approves an organisation request, the system SHALL create an
invitation for the requester and SHALL show its link on the organisation-requests
page, so the admin can pass it on.

#### Scenario: Approve shows the invitation link

- **WHEN** a server admin approves a pending request
- **THEN** the organisation is created, an invitation is created, and its link is shown

#### Scenario: The link can be used to join

- **WHEN** the requester opens the shown invitation link and registers
- **THEN** they become a member of the new organisation
