# QR Workflow Specification

## Purpose

Answer "Where is...?" for an article: scan or search it and show its current
storage location and its default location, with a one-click store to the
default.

## Requirements

### Requirement: Where is an article

The system SHALL show an article's current storage location and its default
location when the user scans or searches for it.

#### Scenario: Look up by code

- **WHEN** the user scans or enters an article code
- **THEN** the article's current location and default location are shown

#### Scenario: Search by name

- **WHEN** the user types a name
- **THEN** matching articles are suggested

#### Scenario: Unknown article

- **WHEN** no article matches the query
- **THEN** the system shows "No article found"

### Requirement: Store to the default location

The system SHALL offer a one-click store to the article's default location when
one exists.

#### Scenario: Store to default

- **WHEN** the user stores an article to its default location
- **THEN** the article is stored there and the view refreshes
