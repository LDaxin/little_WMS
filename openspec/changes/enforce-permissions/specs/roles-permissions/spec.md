## ADDED Requirements

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
