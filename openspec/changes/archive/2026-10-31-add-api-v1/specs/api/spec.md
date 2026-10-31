## ADDED Requirements

### Requirement: Read-only REST API

The system SHALL expose a read-only REST API under `/api/v1/` for the main
models (articles, article bases, article types, storages, storage types,
locations, tags, spaces, occasions, notifications), listing and retrieving them.

#### Scenario: List articles

- **WHEN** an authorised user requests `/api/v1/articles/`
- **THEN** the articles of the active organisation are returned as JSON

#### Scenario: Retrieve an article

- **WHEN** an authorised user requests an article's detail endpoint
- **THEN** the article is returned as JSON

### Requirement: API permissions

The API SHALL require authentication and SHALL gate each endpoint by the role
system: the HTTP method maps to a role action (view/create/edit/delete) and the
endpoint maps to a permission area.

#### Scenario: Unauthenticated request

- **WHEN** an unauthenticated client requests the API
- **THEN** the request is rejected

#### Scenario: Missing permission

- **WHEN** an authenticated user without the area's view permission requests it
- **THEN** the request is rejected with 403
