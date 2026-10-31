## ADDED Requirements

### Requirement: Notification triggers

The system SHALL provide a checks layer that scans for due items and yields
findings, independent of notifications, and a command that turns those findings
into notifications for the responsible roles. The triggers SHALL be
`expiry_date_reached`, `maintenance_due`, and `minimum_stock_undercut`.

#### Scenario: Expiry trigger

- **WHEN** an article expires within the threshold
- **THEN** a finding is produced and a notification is created for the responsible roles

#### Scenario: Maintenance trigger

- **WHEN** a maintenance entry is due
- **THEN** a finding is produced and a notification is created

#### Scenario: Low-stock trigger

- **WHEN** an article's stock is below its minimum
- **THEN** a finding is produced and a notification is created

#### Scenario: No duplicates

- **WHEN** the command runs again while a finding is still open
- **THEN** no second notification is created for the same finding
