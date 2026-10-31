## ADDED Requirements

### Requirement: Maintenance entries

The system SHALL let a user record a maintenance due date for an article. A
maintenance entry SHALL be a calendar entry of type "maintenance" linked to the
article. The article's mini calendar SHALL list its maintenance entries.

#### Scenario: Add a maintenance entry

- **WHEN** the user adds a maintenance entry for an article
- **THEN** a calendar entry of type "maintenance" linked to the article is created

#### Scenario: Maintenance appears in the article mini calendar

- **WHEN** an article has a maintenance entry
- **THEN** the article detail lists it in the mini calendar

#### Scenario: Maintenance appears in the calendar

- **WHEN** a maintenance entry exists
- **THEN** it is listed in the calendar view

#### Scenario: Permission missing

- **WHEN** a user without `article.edit_all` adds a maintenance entry
- **THEN** the system responds with 403
