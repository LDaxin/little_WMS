## Why

§17 lists backup. The system has no data backup, yet the README warns that
changes may break saved data. A full SQLite backup is the smallest, most
valuable safety net before the system is used with real data.

## What Changes

- A consistent SQLite backup via `VACUUM INTO`.
- A "Download backup" action on the server settings page (superuser).
- A `backup` management command for manual or scheduled use.

## Capabilities

### New Capabilities

- `backup`: full SQLite database backup (download and command).

### Modified Capabilities

<!-- none -->

## Impact

- New `hub/backup.py`, a management command, a server-settings action, tests.
- **Deferred**: restore, per-organisation export/import (Level 2), scheduling
  and retention, non-SQLite databases.
