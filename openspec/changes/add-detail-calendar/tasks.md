## 1. Calendar data and month grid (point 1)

- [x] 1.1 Add a `detail_calendar_view` (`calendar` default, `list`) setting to the user profile with a migration and the Preferences form
- [x] 1.2 Build the calendar items for an article from its `CalendarEntry`s (maintenance, loans, occasion entries via the packlist) plus the expiry date, each with a type, start and end
- [x] 1.3 Add a helper that builds the weeks and day cells for a month and places each item as a bar (wrapped per week, with lanes for overlaps) or a dot
- [x] 1.4 Render the month grid in `articleCalendar.html`: month header, weekday row, day cells, bars/dots, legend, today and week highlighting
- [x] 1.5 Add the grid/list switch (per-user setting, like the accordion/tabs toggle); keep the list over the same items

## 2. Month scrolling and lazy loading (point 2)

- [x] 2.1 Put the months in a scrollable area with a sticky month header
- [x] 2.2 Add sentinels that load the previous/next month on `revealed` (HTMX) and append/prepend the block
- [x] 2.3 Compensate the scroll position when a month is prepended
- [x] 2.4 Add a "Today" action that scrolls to the current month

## 3. Period selection and term creation (point 3)

- [ ] 3.1 Client-side selection in the grid: first tap, same day (single), other day (range), × / outside to cancel
- [ ] 3.2 Add an endpoint that checks a selected period for overlaps with the article's entries and returns the conflict popup or the action chooser
- [ ] 3.3 Action chooser (maintenance / lend / borrow) opens the matching form in an overlay, pre-filled with the dates
- [ ] 3.4 On save, create the entry and refresh the calendar

## 4. Term preview, open, edit, delete (point 4)

- [ ] 4.1 Preview a day's terms on tap; open the term in an overlay on the second tap
- [ ] 4.2 Add endpoints to edit (title/start/end) and delete a `CalendarEntry`
- [ ] 4.3 Entry overlay: edit form plus delete; an occasion links to its page; the expiry date is display-only with a link to the article field

## 5. Tests and verification

- [ ] 5.1 Tests: month grid (bars/dots, colours), lazy loading, the conflict check, entry edit/delete, switch resolution
- [ ] 5.2 Run the full suite in Docker; must be green
- [ ] 5.3 Rebuild Docker and report how to test
