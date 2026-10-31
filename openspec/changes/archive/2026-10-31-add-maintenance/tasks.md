## 1. Model

- [x] 1.1 `CalendarEntry.article` (nullable FK) + migration

## 2. View and template

- [x] 2.1 `addMaintenance` view + url
- [x] 2.2 Article detail: "Add maintenance" form
- [x] 2.3 Mini calendar lists maintenance entries

## 3. Tests

- [x] 3.1 Adding a maintenance entry creates the calendar entry
- [x] 3.2 It appears in the article mini calendar
- [x] 3.3 It appears in the calendar view
- [x] 3.4 Permission (403 without `article.edit_all`)

## 4. Verify

- [x] 4.1 Full test suite green in Docker
- [x] 4.2 Rebuild Docker for manual testing
