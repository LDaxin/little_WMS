## 1. Remove offers

- [x] 1.1 Remove `LoanOffer` / `LoanOfferItem` (models, views, urls, template, tests)
- [x] 1.2 Migration

## 2. Share link permissions

- [x] 2.1 `ShareLink.permissions` + `requires_confirmation`
- [x] 2.2 Share form: allow borrowing + needs confirmation
- [x] 2.3 Public view: borrow action (pending/active)

## 3. Tests

- [x] 3.1 Borrow via a link creates a loan
- [x] 3.2 Confirmation → pending
- [x] 3.3 No borrow permission → no borrow

## 4. Verify

- [x] 4.1 Full test suite green in Docker
- [x] 4.2 Rebuild Docker for manual testing
