## 1. Model

- [x] 1.1 `EmailPreference` model (user, category, subscribed) + migration

## 2. Service

- [x] 2.1 `is_subscribed(user, category)` / `set_subscription(...)`

## 3. Enforcement

- [x] 3.1 `hub.mail.send(..., category=None)` skips opted-out categories

## 4. Wiring

- [x] 4.1 `notify()` sends email with category `notifications`
- [x] 4.2 Invitation email uses category `invitations`

## 5. UI

- [x] 5.1 `/email-preferences/` page with per-category checkboxes + link

## 6. Tests

- [x] 6.1 Preference default and toggle
- [x] 6.2 Mail service skips opted-out category, sends subscribed
- [x] 6.3 Notification sends email; opt-out and unverified skip

## 7. Verify

- [x] 7.1 Full test suite green in Docker
- [x] 7.2 Rebuild Docker for manual testing
