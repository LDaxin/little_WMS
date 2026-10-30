# Storage Management Specification

## Purpose

Manage storage locations: storage types, hierarchical storages with an owning
space and code, their contents, and storing/removing articles into them.

## Requirements

### Requirement: Storage types and storages

The system SHALL let an administrator define storage types and create storages
with a name, a type, an optional parent, an optional location, tags, and a code.

#### Scenario: Create a storage

- **WHEN** the user adds a storage
- **THEN** a storage with its own space (`s0…`) and code is created

#### Scenario: Hierarchical storages

- **WHEN** a storage has a parent
- **THEN** its display name is the parent path plus its own name

### Requirement: Storage contents

The system SHALL show the articles currently stored in a storage location.

#### Scenario: View contents

- **WHEN** the user opens a storage
- **THEN** the stock lines stored in that storage's space are listed

### Requirement: Store and remove into a storage

The system SHALL store an article into a storage and remove it again, warning
when the storage's composition expects a different article.

#### Scenario: Store into a storage

- **WHEN** the user stores an article into a storage
- **THEN** the article's quantity is moved into that storage's space

#### Scenario: Composition warning

- **WHEN** the article does not match the storage's composition
- **THEN** the system warns and requires confirmation before storing

### Requirement: Delete a storage

The system SHALL soft-delete a storage and detach its children instead of
deleting them.

#### Scenario: Delete a storage with children

- **WHEN** the user deletes a storage that has child storages
- **THEN** the storage is deleted and its children are re-parented to no parent
