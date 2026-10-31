## 1. Service

- [x] 1.1 `hub/backup.py` `create_backup(path)` via `VACUUM INTO` (SQLite only)

## 2. Command

- [x] 2.1 `manage.py backup [path]`

## 3. UI

- [x] 3.1 "Download backup" action on the server settings page (superuser)

## 4. Tests

- [x] 4.1 Backup file is created and is a valid SQLite database
- [x] 4.2 Download returns the file; non-superuser gets 403
- [x] 4.3 Command writes a backup

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker and restart the container
