# Organisations Specification

## Purpose

Support multiple organisations: every object belongs to one organisation, a user
can be a member of several organisations with a different role in each, and all
work happens within the active organisation.
## Requirements
### Requirement: Objects belong to an organisation

The system SHALL assign every organisation-scoped object to exactly one
organisation, defaulting to the active organisation.

#### Scenario: New object uses the active organisation

- **WHEN** an object is created while an organisation is active
- **THEN** the object is assigned to that organisation

### Requirement: Membership

The system SHALL let a user belong to several organisations, with one membership
profile per organisation and a role per organisation.

#### Scenario: Multiple memberships

- **WHEN** a user is a member of two organisations
- **THEN** the user has two membership profiles, one per organisation

#### Scenario: Unique membership

- **WHEN** a membership for the same user and organisation already exists
- **THEN** a second one is rejected

### Requirement: Active organisation

The system SHALL keep the active organisation in the session, select it at login,
and let the user switch it.

#### Scenario: Single membership

- **WHEN** a user belongs to exactly one organisation
- **THEN** that organisation is used directly after login

#### Scenario: Multiple memberships

- **WHEN** a user belongs to several organisations
- **THEN** the user is asked which organisation to use

#### Scenario: Switch organisation

- **WHEN** the user switches to another organisation they belong to
- **THEN** the active organisation changes and the view updates

### Requirement: Queries are scoped to the active organisation

The system SHALL scope reads to the active organisation, so a user never sees
objects from another organisation.

#### Scenario: Isolation

- **WHEN** an organisation is active
- **THEN** queries return only objects of that organisation

#### Scenario: No active organisation

- **WHEN** no organisation is active (e.g. admin, shell, tests)
- **THEN** queries are not filtered

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

