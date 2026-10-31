## ADDED Requirements

### Requirement: API write operations

The API SHALL allow creating, updating, and deleting locations, tags, article
types, and storage types. The `code` and `organisation` fields SHALL be
read-only. Deleting SHALL soft-delete the object.

#### Scenario: Create a location

- **WHEN** an authorised user POSTs a location
- **THEN** the location is created

#### Scenario: Update a tag

- **WHEN** an authorised user PATCHes a tag
- **THEN** the tag is updated

#### Scenario: Delete a storage type

- **WHEN** an authorised user DELETEs a storage type
- **THEN** it is soft-deleted

#### Scenario: Missing write permission

- **WHEN** a user without the area's create permission POSTs
- **THEN** the request is rejected with 403
