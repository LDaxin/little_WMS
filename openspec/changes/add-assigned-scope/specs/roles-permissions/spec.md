## ADDED Requirements

### Requirement: The assigned scope is enforced for articles

The system SHALL allow an article action when the role has the `_all` scope, or
when it has the `_assigned` scope and the article is assigned to the user. A
user whose role has only the `_assigned` scope SHALL see only assigned articles
in lists.

#### Scenario: All scope

- **WHEN** the role has `article.view_all`
- **THEN** the user may view every article

#### Scenario: Assigned scope on a list

- **WHEN** the role has only `article.view_assigned`
- **THEN** the article list shows only articles assigned to the user

#### Scenario: Assigned scope on an unassigned object

- **WHEN** the role has only `article.edit_assigned` and the article is not assigned to the user
- **THEN** editing is forbidden (403)

#### Scenario: Assigned scope on an assigned object

- **WHEN** the role has `article.move_assigned` and the article is assigned to the user
- **THEN** the user may move it
