## ADDED Requirements

### Requirement: Category opt-out

The central mail service SHALL skip a message whose category the recipient has
opted out of, and SHALL log the skip. A message without a category is not
subject to opt-out.

#### Scenario: Opted out category

- **WHEN** code sends a message with a category the recipient opted out of
- **THEN** the message is skipped and a warning is logged

#### Scenario: Subscribed category

- **WHEN** code sends a message with a category the recipient is subscribed to
- **THEN** the message is sent

#### Scenario: No category

- **WHEN** code sends a message without a category
- **THEN** the opt-out does not apply
