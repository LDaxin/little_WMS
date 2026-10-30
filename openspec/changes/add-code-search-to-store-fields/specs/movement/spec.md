## ADDED Requirements

### Requirement: Store target field finds by code or name

The store-target field on an article SHALL find the target storage or container
by code OR by name (live suggestions), and SHALL offer the QR scanner.

#### Scenario: Search by name

- **WHEN** the user types a name in the store-target field
- **THEN** matching storages or containers are suggested and can be picked to store there

#### Scenario: Scan a target code

- **WHEN** the user scans a target code
- **THEN** the field accepts it and the article can be stored
