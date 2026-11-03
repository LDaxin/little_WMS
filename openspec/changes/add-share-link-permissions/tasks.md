## 1. Permission check

- [x] 1.1 `LINK_ACTIONS` mapping + `link_codenames`
- [x] 1.2 `has_perm(..., link=None)` uses the link context

## 2. Share view

- [x] 2.1 `ShareLink.can(action)`
- [x] 2.2 Resolve the effective source and gate the borrow action
- [x] 2.3 `shareLinkMode` view + URL

## 3. UI

- [x] 3.1 Toggle in the share view (logged-in only)

## 4. Tests

- [x] 4.1 Anonymous uses the link permissions
- [x] 4.2 Logged-in "link" mode uses the link permissions
- [x] 4.3 Logged-in "mine" mode uses the role
- [x] 4.4 Toggle switches the mode

## 5. Verify

- [x] 5.1 Full suite green in Docker
- [x] 5.2 Rebuild + restart
