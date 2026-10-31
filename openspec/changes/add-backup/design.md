## Context

§17 lists backup. The database is SQLite by default. `VACUUM INTO` produces a
consistent copy of a live database, which is exactly what a backup needs.

## Goals / Non-Goals

**Goals:**

- A consistent full backup of the SQLite database.
- Download it from the server settings page (superuser).
- A `backup` management command.

**Non-Goals:**

- Restore, per-organisation export/import, scheduling, retention.
- Non-SQLite databases.

## Decisions

### Decision 1: `VACUUM INTO`

`VACUUM INTO 'file'` writes a consistent copy without locking the database for
long, unlike copying the file. It is SQLite-only; other engines raise a clear
error.

### Decision 2: Download reads the backup into memory

The backup is written to a temporary file, read, and returned as a download.
For a personal WMS the database is small, so this avoids temp-file lifecycle
issues.

### Decision 3: A management command

`manage.py backup [path]` writes the backup to a path (default under `data/`),
so it can be run manually or from a scheduler.

## Risks / Trade-offs

- [In-memory download] → fine for a small database; a streaming download is a
  later change if it grows.
- [No restore yet] → the backup is a file the operator can restore manually.

## Migration Plan

- None.
