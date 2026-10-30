## 1. Model

- [x] 1.1 Add `OccasionTemplate` (organisation, name, occasion_type, default_packlist)
- [x] 1.2 Migration

## 2. Views and URLs

- [x] 2.1 Template list + add + delete views/urls
- [x] 2.2 `saveOccasionAsTemplate` (POST on the occasion detail)
- [x] 2.3 `addOccasion` accepts an optional `template` and copies its packlist

## 3. Templates (HTML)

- [x] 3.1 `templates.html` (list, add, delete)
- [x] 3.2 Occasion detail: "Save as template" action
- [x] 3.3 `occasionForm.html`: template selector

## 4. Tests

- [x] 4.1 Model `str`
- [x] 4.2 Save as template captures type + packlist
- [x] 4.3 Create from template copies the packlist
- [x] 4.4 Template list / delete
- [x] 4.5 Permissions (403 without `occasion.create_all`)

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker for manual testing
