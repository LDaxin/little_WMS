## ADDED Requirements

### Requirement: Notification rules

The system SHALL store notification rules per organisation and trigger type,
each with an active flag, an optional threshold, recipients (roles and
individual users), and channels (in-app, email).

#### Scenario: Create a rule

- **WHEN** an admin creates a rule for a trigger with a role and the in-app channel
- **THEN** the rule is stored and applies to that trigger

#### Scenario: Inactive rule

- **WHEN** a rule is inactive
- **THEN** it is not applied

### Requirement: Apply rules to triggers

The trigger command SHALL resolve recipients from the active rules for a
finding's trigger type and SHALL create notifications on the configured
channels. When no rule exists for a trigger, the command SHALL keep the default
(the `article_view_all` role, in-app).

#### Scenario: Rule recipients

- **WHEN** a finding matches an active rule
- **THEN** the users of its roles and its individual users are notified

#### Scenario: Email channel

- **WHEN** a rule has the email channel
- **THEN** the recipients also receive an email

#### Scenario: No rule

- **WHEN** no rule exists for a trigger
- **THEN** the default recipients are notified in-app

### Requirement: Manage rules

The system SHALL provide a page to list, add, edit, and delete rules, requiring
the `notification.manage_rules` permission.

#### Scenario: List rules

- **WHEN** an admin opens the rules page
- **THEN** the rules are listed

#### Scenario: Permission missing

- **WHEN** a user without `notification.manage_rules` opens the rules page
- **THEN** the system responds with 403
