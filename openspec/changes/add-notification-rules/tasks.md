## 1. Model

- [x] 1.1 `NotificationRule` model + migration

## 2. Command

- [x] 2.1 `notify()` gains an `email` flag
- [x] 2.2 `check_notifications` resolves recipients/channels from active rules
- [x] 2.3 Fall back to the default when no rule exists

## 3. UI

- [x] 3.1 Rules list, add, edit, delete (perm `notification.manage_rules`)

## 4. Tests

- [x] 4.1 Rule recipients (roles + users) are notified
- [x] 4.2 Email channel sends; in-app only does not
- [x] 4.3 No rule → default recipients
- [x] 4.4 Rules page CRUD + permission

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker and restart the container
