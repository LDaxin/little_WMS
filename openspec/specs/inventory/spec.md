# Inventory Specification

## Purpose

Run an inventory of a storage location: scan the location to set the scope, scan
the articles found there, track progress, flag deviations, and export a report.

## Requirements

### Requirement: Inventory scope

The system SHALL let the user start an inventory by scanning a storage location,
which becomes the scope of the inventory.

#### Scenario: Scan a location

- **WHEN** the user scans a storage location
- **THEN** it becomes the inventory scope and the expected articles are listed

#### Scenario: Scan an article before a location

- **WHEN** the user scans an article before a location is set
- **THEN** the system shows "Scan a location first"

### Requirement: Expected articles and progress

The system SHALL list the articles expected in the scope (the current stock
there) and SHALL show how many have been scanned.

#### Scenario: Mark an article as found

- **WHEN** the user scans an article that is expected in the scope
- **THEN** it is marked as found and the progress count increases

#### Scenario: Not found yet

- **WHEN** an expected article has not been scanned
- **THEN** it is shown as "not found yet"

### Requirement: Deviations

The system SHALL flag a scanned article that is not expected in the scope,
showing where it actually is.

#### Scenario: Article belongs elsewhere

- **WHEN** the user scans an article that is stored in a different location
- **THEN** the system flags it as a deviation and shows its actual location

### Requirement: Report export

The system SHALL export the inventory result as CSV.

#### Scenario: Export the report

- **WHEN** the user exports the inventory
- **THEN** a CSV with the expected articles (found / not found) and the deviations is downloaded
