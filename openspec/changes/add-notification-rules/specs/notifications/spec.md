## ADDED Requirements

### Requirement: Configurable trigger recipients

The trigger command SHALL use the configured notification rules to decide the
recipients and channels of a finding, falling back to the default when no rule
exists.

#### Scenario: Configured recipients

- **WHEN** a finding's trigger has an active rule
- **THEN** the rule's recipients and channels are used

#### Scenario: Default recipients

- **WHEN** a finding's trigger has no rule
- **THEN** the `article_view_all` role is notified in-app
