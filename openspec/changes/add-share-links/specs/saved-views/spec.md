## ADDED Requirements

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
