## ADDED Requirements

### Requirement: Recurring occasions

The system SHALL let a user make an occasion recurring from its detail page by
choosing a frequency, an interval, and an end condition. The system SHALL
generate the future occasions, each with its own packlist copied from the head
occasion.

#### Scenario: Make an occasion recurring

- **WHEN** the user makes an occasion recurring
- **THEN** the future occasions are generated with the packlist copied from the head

#### Scenario: An occasion is already recurring

- **WHEN** the user tries to make an already-recurring occasion recurring again
- **THEN** no second rule is created
