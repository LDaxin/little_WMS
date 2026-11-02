## 1. Model

- [x] 1.1 One `Loan` model with `direction` and `calendar_entry`
- [x] 1.2 Migration (remove `Lending`, rebuild `Loan`)

## 2. Views & URLs

- [x] 2.1 Unify `loans/views.py` (list, lend, borrow, return, confirm)
- [x] 2.2 URLs; drop `/lendings/`

## 3. Templates

- [x] 3.1 Merge `lendings.html` into `loans.html`
- [x] 3.2 Hub tile → `/loans/`

## 4. Callers

- [x] 4.1 `notifications/checks.py`: one overdue path
- [x] 4.2 `savedviews/views.py`: share-link flow
- [x] 4.3 `security/views.py`: data export

## 5. Tests

- [x] 5.1 Update loans / notifications / savedviews tests

## 6. Verify

- [x] 6.1 Full suite green in Docker
- [x] 6.2 Rebuild + restart
- [x] 6.3 Update loans spec + RF-001 in the backlog
