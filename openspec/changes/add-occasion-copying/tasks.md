## 1. View and URL

- [x] 1.1 `duplicateOccasion` view + url
- [x] 1.2 Copy the occasion (type, location, participants, packlist, shifted dates)

## 2. Template

- [x] 2.1 Occasion detail: "Duplicate" form with a shift field

## 3. Tests

- [x] 3.1 Duplicate creates a copy with the packlist
- [x] 3.2 Shift moves the dates
- [x] 3.3 Permission (403 without `occasion.create_all`)

## 4. Verify

- [x] 4.1 Full test suite green in Docker
- [x] 4.2 Rebuild Docker for manual testing
