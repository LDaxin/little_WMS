## ADDED Requirements

### Requirement: Create a database backup

The system SHALL create a consistent full backup of the SQLite database using
`VACUUM INTO`. For a non-SQLite database it SHALL report that backup is not
supported.

#### Scenario: Backup a SQLite database

- **WHEN** a backup is created
- **THEN** a consistent copy of the database is written

#### Scenario: Non-SQLite database

- **WHEN** a backup is requested for a non-SQLite database
- **THEN** the system reports that backup is not supported

### Requirement: Download a backup

The system SHALL let a superuser download a backup from the server settings
page.

#### Scenario: Download

- **WHEN** a superuser triggers the backup download
- **THEN** the backup file is returned as a download

#### Scenario: Permission missing

- **WHEN** a non-superuser triggers the backup download
- **THEN** the system responds with 403

### Requirement: Backup command

The system SHALL provide a `backup` management command that writes a backup to
a given path.

#### Scenario: Run the command

- **WHEN** the `backup` command is run with a path
- **THEN** a backup file is written to that path
