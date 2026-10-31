## 1. Model

- [x] 1.1 `loans` app + `Loan` model + migration
- [x] 1.2 `CalendarEntry` entry type `loan`

## 2. Views and URLs

- [x] 2.1 Create a loan (from the article detail)
- [x] 2.2 Loan list
- [x] 2.3 Record a return

## 3. Templates

- [x] 3.1 Loan list template
- [x] 3.2 Article detail: "Lend" form

## 4. Tests

- [x] 4.1 Create a loan (calendar entry created)
- [x] 4.2 The loan appears in the calendar
- [x] 4.3 Return sets the status
- [x] 4.4 Permission (403 without `article.move_all`)

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker for manual testing
