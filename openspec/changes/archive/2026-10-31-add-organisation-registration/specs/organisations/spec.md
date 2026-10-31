## ADDED Requirements

### Requirement: Registration policy

The system SHALL have a server-level registration policy with the values
`open`, `invite`, and `request`, settable by a server admin.

#### Scenario: Set the policy

- **WHEN** a server admin sets the registration policy
- **THEN** the public registration page follows it

### Requirement: Register an organisation

The system SHALL provide a public registration page that follows the policy:
with `open` it creates the organisation and its first admin; with `request` it
records an organisation request; with `invite` it shows that registration is
invite-only.

#### Scenario: Open registration

- **WHEN** the policy is `open` and a visitor registers an organisation
- **THEN** the organisation and its first admin are created and the admin is logged in

#### Scenario: Request registration

- **WHEN** the policy is `request` and a visitor submits a request with a reason
- **THEN** an organisation request is recorded as pending

#### Scenario: Invite-only

- **WHEN** the policy is `invite`
- **THEN** the registration page shows that registration is invite-only

### Requirement: Review organisation requests

The system SHALL let a server admin list organisation requests and approve or
reject them. Approving SHALL create the organisation.

#### Scenario: Approve a request

- **WHEN** a server admin approves a pending request
- **THEN** the organisation is created and the request is marked approved

#### Scenario: Reject a request

- **WHEN** a server admin rejects a pending request
- **THEN** the request is marked rejected and no organisation is created

#### Scenario: Not a server admin

- **WHEN** a non-superuser opens the request review page
- **THEN** the system responds with 403
