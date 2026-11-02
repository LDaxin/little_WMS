## 1. Model

- [x] 1.1 Remove `Article.ownership` field and choices
- [x] 1.2 Add the derived `ownership` property
- [x] 1.3 Migration

## 2. Callers

- [x] 2.1 Remove the write sites in `loans/views.py`
- [x] 2.2 Remove the write site in `savedviews/views.py`
- [x] 2.3 Drop `ownership` from the article form excludes

## 3. API

- [x] 3.1 `ownership` read-only on the article serializer

## 4. Tests

- [x] 4.1 Existing loan tests stay green
- [x] 4.2 Pending loan counts as borrowed; returned loan as owned

## 5. Verify

- [x] 5.1 Full suite green in Docker
- [x] 5.2 Rebuild + restart
