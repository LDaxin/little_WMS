## ADDED Requirements

### Requirement: Store-article field finds by code or name

The store-article field on a storage SHALL find the article by code OR by name
(live suggestions), and SHALL offer the QR scanner.

#### Scenario: Search by name

- **WHEN** the user types a name in the store-article field
- **THEN** matching articles are suggested and can be picked to store there

#### Scenario: Scan an article code

- **WHEN** the user scans an article code
- **THEN** the field accepts it and the article can be stored
