## ADDED Requirements

### Requirement: Per-category email preference

The system SHALL store a per-user, per-category email preference. A user SHALL
be subscribed by default; a missing preference means subscribed.

#### Scenario: Default subscribed

- **WHEN** a user has no preference for a category
- **THEN** they are treated as subscribed

#### Scenario: Opt out

- **WHEN** a user opts out of a category
- **THEN** they are treated as unsubscribed for that category only

### Requirement: Manage email preferences

The system SHALL provide a page where a user toggles each email category.

#### Scenario: Toggle a category

- **WHEN** a user unchecks a category and saves
- **THEN** the preference is stored and the category is unsubscribed

#### Scenario: Requires login

- **WHEN** a logged-out visitor opens the preferences page
- **THEN** they are redirected to login
