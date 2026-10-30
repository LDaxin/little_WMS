# Roles and Permissions Specification

## Purpose

Give each organisation its own permission concept: a catalogue of atomic
permissions, roles as named collections of permissions, role templates, and
permission checks scoped to the active organisation.
## Requirements
### Requirement: Permission catalogue

The system SHALL define a catalogue of atomic permissions as
`area.action_scope` (e.g. `article.view_all`), materialised as Django
`auth.Permission` entries.

#### Scenario: Catalogue is available

- **WHEN** the system is migrated
- **THEN** the catalogue permissions exist as `auth.Permission` entries

### Requirement: Roles are per organisation

The system SHALL let each organisation define roles as named collections of
catalogue permissions, and SHALL provide pre-configured role templates.

#### Scenario: Create a role from a template

- **WHEN** the user creates a role from a template
- **THEN** a new role with the template's permissions is created for the organisation

#### Scenario: Edit a role

- **WHEN** the user edits a role's permission matrix
- **THEN** the role's permissions are updated

### Requirement: Permission checks are organisation-scoped

The system SHALL evaluate a permission against the user's role in the active
organisation, and SHALL grant everything to superusers.

#### Scenario: Role per organisation

- **WHEN** a user has different roles in two organisations
- **THEN** a permission check uses the role of the organisation it is evaluated for

#### Scenario: Superuser

- **WHEN** the user is a superuser
- **THEN** every permission check passes

### Requirement: Roles and users are managed by permission

The system SHALL restrict the roles and users management pages to users holding
the matching permission.

#### Scenario: Without permission

- **WHEN** a user without the role-management permission opens the roles page
- **THEN** the system responds with 403

#### Scenario: Assign a role

- **WHEN** a user with the permission assigns a role to a member
- **THEN** the member's role in the active organisation is updated

### Requirement: Views are protected by their permission

The system SHALL guard every view with the catalogue permission that matches the
action it performs, and SHALL respond with 403 when the user does not hold that
permission in the active organisation. Superusers SHALL pass every check.

#### Scenario: View permission missing

- **WHEN** a user without `article.view_all` opens the article list or detail
- **THEN** the system responds with 403

#### Scenario: View permission granted

- **WHEN** a user with `article.view_all` opens the article list
- **THEN** the list is shown

#### Scenario: Create, edit and delete

- **WHEN** a user opens the add, update, or delete view without the matching `create`, `edit`, or `delete` permission
- **THEN** the system responds with 403

#### Scenario: Moving articles

- **WHEN** a user uses movement or stores/removes an article without `article.move_all`
- **THEN** the system responds with 403

#### Scenario: Export

- **WHEN** a user requests a CSV or QR-sheet export without the matching `export` permission
- **THEN** the system responds with 403

#### Scenario: Superuser

- **WHEN** a superuser opens any protected view
- **THEN** access is granted

