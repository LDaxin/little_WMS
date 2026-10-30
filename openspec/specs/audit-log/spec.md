# Audit Log Specification

## Purpose

Record every relevant action on objects in a unified audit log, show an object's
history, expose a filterable admin log, and support configurable retention.

## Requirements

### Requirement: Unified audit log

The system SHALL write one audit entry per action, capturing the user, the
organisation, the timestamp, the action, the affected object, and the changes.

#### Scenario: Log an action

- **WHEN** an object is created, updated, deleted, moved, or removed
- **THEN** an audit entry is written with the acting user and the changes

#### Scenario: Changes detail

- **WHEN** a field changes
- **THEN** the entry records the old and new value for that field

### Requirement: Object history

The system SHALL show an object's recent audit entries as a timeline on its
detail page.

#### Scenario: Article timeline

- **WHEN** the user opens an article
- **THEN** its recent audit entries are shown as a history timeline

### Requirement: Admin log with filters

The system SHALL provide a read-only admin view of the audit log with filters
for action, user, content type, organisation, and date.

#### Scenario: Filter the log

- **WHEN** an administrator opens the audit log in the admin
- **THEN** entries can be filtered by action, user, type, and date, and cannot be edited

### Requirement: Retention

The system SHALL support a per-organisation retention period and SHALL purge
entries older than it.

#### Scenario: Purge old entries

- **WHEN** the purge command runs for an organisation with a retention period
- **THEN** entries older than the period are deleted and newer ones are kept

#### Scenario: Keep forever

- **WHEN** an organisation has no retention period
- **THEN** no entries are purged
