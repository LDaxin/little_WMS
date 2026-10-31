# demo-seed Specification

## Purpose
TBD - created by archiving change update-demo-seed. Update Purpose after archive.
## Requirements
### Requirement: Demo seed

The system SHALL provide a `seed_demo` management command that creates a small
realistic development dataset: article types, storages, tags, articles,
locations, occasion types, occasions with a packlist, and occasion templates.
The command SHALL be idempotent.

#### Scenario: Seed a fresh database

- **WHEN** `seed_demo` runs on an empty database
- **THEN** the demo dataset is created

#### Scenario: Seed is idempotent

- **WHEN** `seed_demo` runs twice
- **THEN** the second run creates no duplicates

