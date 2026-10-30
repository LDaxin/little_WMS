# Code System Specification

## Purpose

Provide unique codes for articles, storages, and locations: pre-generated codes,
code assignment, canonical links by code, and code export.

## Requirements

### Requirement: Unique codes

The system SHALL generate unique codes with a prefix that identifies the kind of
object (`a0` article, `s0` storage, `l0` location) and SHALL track whether a code
is used.

#### Scenario: Generate codes

- **WHEN** the user generates codes of a kind
- **THEN** that many unused codes with the matching prefix are created

#### Scenario: Assign a code

- **WHEN** a code is assigned to an object
- **THEN** the code is marked used

### Requirement: Canonical links by code

The system SHALL resolve a code to its object via short links (`/a/<code>`,
`/s/<code>`, `/l/<code>`).

#### Scenario: Resolve an article code

- **WHEN** the user opens `/a/<code>` for an existing article
- **THEN** the system redirects to that article's page

#### Scenario: Unknown code

- **WHEN** the user opens a short link for a code that does not exist
- **THEN** the system responds with 404

### Requirement: Export codes

The system SHALL export selected unused codes as CSV.

#### Scenario: Export codes

- **WHEN** the user exports selected codes
- **THEN** a CSV with prefix, code, and kind is downloaded
