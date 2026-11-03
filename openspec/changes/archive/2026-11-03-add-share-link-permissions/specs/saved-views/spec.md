## ADDED Requirements

### Requirement: Share-link permissions are a permission source

The system SHALL let a permission check take its permissions from a share link
instead of the user's role. A share link's action list SHALL map to catalogue
permissions (`view` to `article.view_all`, `borrow` to `article.move_all`).

#### Scenario: Link grants the action

- **WHEN** a permission is checked with a link that grants the matching action
- **THEN** the check passes regardless of the user's role

#### Scenario: Link does not grant the action

- **WHEN** a permission is checked with a link that does not grant the matching action
- **THEN** the check fails

### Requirement: A logged-in user can switch the permission source

The share view SHALL use the link's permissions by default. A logged-in user
SHALL be able to switch to their own role's permissions for that link, and back.

#### Scenario: Anonymous visitor

- **WHEN** an anonymous visitor opens a share link
- **THEN** the link's permissions apply

#### Scenario: Switch to own permissions

- **WHEN** a logged-in user switches the share view to their own permissions
- **THEN** the user's role decides the available actions

#### Scenario: Switch back

- **WHEN** the user switches back to the link's permissions
- **THEN** the link's permissions apply again
