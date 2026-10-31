## 1. App and model

- [x] 1.1 Create the `notifications` app (apps.py, `INSTALLED_APPS`, urls)
- [x] 1.2 `Notification` model + migration

## 2. Service

- [x] 2.1 `notify(user, ...)` and `notify_roles(organisation, codename, ...)`

## 3. Center

- [x] 3.1 Notification page (list, mark one read, mark all read)
- [x] 3.2 Bell + dropdown in the header
- [x] 3.3 Context processor for the unread count

## 4. Tests

- [x] 4.1 `notify` creates an unread notification
- [x] 4.2 `notify_roles` notifies holders of a permission
- [x] 4.3 The page lists notifications; mark read / mark all read
- [x] 4.4 Permission (403 without `notification.view_all`)

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker for manual testing
