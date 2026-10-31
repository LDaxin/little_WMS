## 1. Model and service

- [x] 1.1 `Notification.dedupe_key` + migration
- [x] 1.2 `notify` / `notify_roles` accept a `dedupe_key` and skip duplicates

## 2. Checks

- [x] 2.1 `Finding` + `run_checks(organisation)`
- [x] 2.2 `expiry_findings`, `maintenance_findings`, `low_stock_findings`

## 3. Command

- [x] 3.1 `check_notifications` management command

## 4. Tests

- [x] 4.1 Each check yields a finding
- [x] 4.2 The command creates notifications for the responsible roles
- [x] 4.3 Dedupe: a second run creates no duplicate

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker for manual testing
