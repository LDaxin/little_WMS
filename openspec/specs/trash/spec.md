# trash Specification

## Purpose
TBD - created by archiving change add-trash. Update Purpose after archive.
## Requirements
### Requirement: Trash view

The system SHALL provide a trash view that lists the soft-deleted objects of the
active organisation, grouped by model.

#### Scenario: List deleted objects

- **WHEN** a user with `trash.view_all` opens the trash
- **THEN** the soft-deleted objects of the active organisation are listed

#### Scenario: View permission missing

- **WHEN** a user without `trash.view_all` opens the trash
- **THEN** the system responds with 403

### Requirement: Restore from trash

The system SHALL let a user restore a soft-deleted object, restoring its whole
change set.

#### Scenario: Restore an object

- **WHEN** a user with `trash.restore_all` restores a deleted object
- **THEN** the object is no longer deleted and appears again in its normal views

#### Scenario: Restore permission missing

- **WHEN** a user without `trash.restore_all` restores an object
- **THEN** the system responds with 403

### Requirement: Permanently delete from trash

The system SHALL let a user permanently delete a soft-deleted object.

#### Scenario: Permanently delete an object

- **WHEN** a user with `trash.delete_forever_all` permanently deletes an object
- **THEN** the object is removed from the database

#### Scenario: Permanent-delete permission missing

- **WHEN** a user without `trash.delete_forever_all` permanently deletes an object
- **THEN** the system responds with 403

