## 1. Rename

- [x] 1.1 `loans.Loan` → `loans.Lending` (model, related_name, views, urls, templates, tests)

## 2. Article

- [x] 2.1 `Article.ownership` + `loan_requires_confirmation`

## 3. Loan (borrow in)

- [x] 3.1 `loans.Loan` model + migration
- [x] 3.2 Create / list / return views + urls + template

## 4. Tests

- [x] 4.1 Borrow from a person / organisation
- [x] 4.2 Return
- [x] 4.3 Permission (403 without `article.move_all`)
- [x] 4.4 Lending still works after the rename

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker for manual testing
