## ADDED Requirements

### Requirement: Storage columns and cards

The storage list SHALL use the shared table/card framework. It SHALL offer the
columns image, name, code, type, parent and location by default, plus optional
columns (contents count, tags). The storage card SHALL show image, name, code,
type, parent and location.

#### Scenario: Default columns

- **WHEN** the storage list is shown with default columns
- **THEN** name, code, type, parent and location are shown

#### Scenario: Storage card

- **WHEN** a storage is shown as a card
- **THEN** the card shows its name, code, type, parent and location
