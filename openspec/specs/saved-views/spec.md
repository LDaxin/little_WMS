# saved-views Specification

## Purpose
TBD - created by archiving change add-saved-views. Update Purpose after archive.
## Requirements
### Requirement: Save a view

The system SHALL let a user save the current query under a name, optionally
shared within the organisation.

#### Scenario: Save a view

- **WHEN** the user saves the current query as a view
- **THEN** a saved view with that name and query is created

### Requirement: List and apply saved views

The system SHALL list the user's own and the organisation's shared saved views,
and SHALL let the user apply one to the article list.

#### Scenario: List views

- **WHEN** the user opens the views page
- **THEN** their own and the shared views are listed

#### Scenario: Apply a view

- **WHEN** the user applies a saved view
- **THEN** the article list shows the view's query results

#### Scenario: Delete a view

- **WHEN** the user deletes their own view
- **THEN** it is removed

