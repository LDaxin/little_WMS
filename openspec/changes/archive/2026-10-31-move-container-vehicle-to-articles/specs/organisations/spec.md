## ADDED Requirements

### Requirement: Standard configuration defaults

The standard article types SHALL include Container and Vehicle (both with
`article_toggle_space`), and the standard storage types SHALL NOT include them,
following the §8 philosophy (movable = article).

#### Scenario: Container and Vehicle are article types

- **WHEN** the standard defaults are loaded
- **THEN** Container and Vehicle are created as article types that can hold articles
