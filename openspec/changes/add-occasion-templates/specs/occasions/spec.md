## ADDED Requirements

### Requirement: Occasion templates

The system SHALL let a user save an occasion as a reusable template that stores
the occasion type and a default packlist (article + quantity). The system SHALL
let a user create an occasion from a template, pre-filling the type and copying
the template's packlist onto the new occasion. The system SHALL let a user list
and delete templates.

#### Scenario: Save an occasion as a template

- **WHEN** the user saves an occasion as a template
- **THEN** a template is created with the occasion's type and its packlist entries

#### Scenario: Create an occasion from a template

- **WHEN** the user creates an occasion and picks a template
- **THEN** the occasion uses the template's type and its packlist is copied from the template

#### Scenario: List and delete templates

- **WHEN** the user opens the template list
- **THEN** the templates are listed, and the user can delete one

#### Scenario: Template permission

- **WHEN** a user without `occasion.create_all` saves or creates from a template
- **THEN** the system responds with 403
