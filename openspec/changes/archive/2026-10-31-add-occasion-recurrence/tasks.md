## 1. Planning app

- [x] 1.1 Create the `planning` app (apps.py, `INSTALLED_APPS`)
- [x] 1.2 Move `CalendarEntry` from `occasion` to `planning`
- [x] 1.3 Add `RecurrenceRule` + `CalendarEntry.recurrence_rule`
- [x] 1.4 Migrations (drop/recreate) + repoint `Occasion.calendar_entry`

## 2. Recurrence

- [x] 2.1 Date-stepping helper (daily/weekly/monthly/yearly)
- [x] 2.2 `recurrence_dates` (bounded by end condition / horizon)
- [x] 2.3 `repeat_occasion` (generate instances, copy the packlist)

## 3. View and template

- [x] 3.1 `repeatOccasion` view + url
- [x] 3.2 Occasion detail: "Repeat" form + series info

## 4. Tests

- [x] 4.1 Date stepping (month-end, leap year)
- [x] 4.2 Generation (yearly + end_after_occurrences)
- [x] 4.3 Instances copy the packlist
- [x] 4.4 Already-recurring guard
- [x] 4.5 Permission

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Dev DB reset + Docker rebuild
