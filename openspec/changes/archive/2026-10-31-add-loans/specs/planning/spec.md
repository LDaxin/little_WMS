## ADDED Requirements

### Requirement: Loan calendar entries

The calendar SHALL support a `loan` entry type, used by loans for their period.

#### Scenario: A loan entry is a calendar entry

- **WHEN** a loan is created
- **THEN** it is backed by a calendar entry of type `loan`
