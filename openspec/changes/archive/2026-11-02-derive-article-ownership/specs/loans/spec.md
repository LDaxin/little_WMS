## ADDED Requirements

### Requirement: Ownership is derived from the open loan

The system SHALL derive an article's ownership from its loans instead of storing
it: an article SHALL be `borrowed` while an open (pending or active) loan with
direction `in` exists, and `owned` otherwise.

#### Scenario: Borrowed in

- **WHEN** an article has an open loan with direction `in`
- **THEN** its ownership is `borrowed`

#### Scenario: Returned

- **WHEN** the article's borrowed-in loan is returned
- **THEN** its ownership is `owned`

#### Scenario: Lent out

- **WHEN** an article is lent out (direction `out`)
- **THEN** its ownership stays `owned`
