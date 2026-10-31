## ADDED Requirements

### Requirement: Calendar entries

The system SHALL store dated calendar entries with a type (occasion,
maintenance, purchase, disposal, inventory, other), a title, a start date, an
optional end date, optional notes, and an optional responsible user. An entry
SHALL belong to the active organisation.

#### Scenario: An occasion is backed by a calendar entry

- **WHEN** an occasion is created
- **THEN** it is backed by a calendar entry of type "occasion"

### Requirement: Recurrence rules

The system SHALL let a calendar entry carry an optional recurrence rule with a
frequency (daily, weekly, monthly, yearly), an interval, and an end condition
(an end date, a number of occurrences, or none). The system SHALL generate the
future entries for a rule, bounded by the end condition (or a horizon when there
is none). For occasion entries the matching occasion and its packlist SHALL be
created as well.

#### Scenario: Generate future entries

- **WHEN** a recurrence rule is applied to a calendar entry
- **THEN** the future entries are created according to the frequency and interval

#### Scenario: End after a number of occurrences

- **WHEN** a rule ends after N occurrences
- **THEN** the series has N entries in total, including the head

#### Scenario: Occasion instances copy the packlist

- **WHEN** a recurring occasion generates a future instance
- **THEN** the instance's packlist is copied from the head occasion
