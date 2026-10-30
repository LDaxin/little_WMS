## ADDED Requirements

### Requirement: Articles can be assigned to users

The system SHALL let a user assign an article to one or more users and SHALL
show the assignees on the article.

#### Scenario: Assign an article

- **WHEN** a user assigns an article to another user
- **THEN** the article is listed as assigned to that user

#### Scenario: Unassign an article

- **WHEN** a user removes an assignee from an article
- **THEN** the article is no longer assigned to that user
