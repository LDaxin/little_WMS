## Why

The article detail's calendar module is a flat list of terms plus three inline
forms. It gives no spatial view of when the article is booked, no way to create
a term by picking a period, and no way to edit or delete existing terms. Users
want to see the article's bookings as a month grid, spot conflicts, and manage
terms directly.

## What Changes

- Replace the flat term list with a **month-grid mini calendar**: a bar spanning
  the days of a range, a dot for a single day, coloured by term type, with a
  legend and clear visual separation.
- A **switch** between the calendar grid and the existing list; the choice is a
  per-user setting.
- The calendar **scrolls** vertically through months and **lazy-loads** the
  neighbouring months in both directions.
- **Create a term by picking a period**: tap a free day to start, tap the same
  day again for a single-day term, or another day for a range (the earlier day
  is the start). The system then checks for **conflicts** and, if there are any,
  shows them in a popup; if the period is free it asks which **action**
  (maintenance / lend / borrow) and opens the matching form in a popup,
  pre-filled with the dates.
- **Preview** an existing term on tap and **open** it in a popup with **edit
  (title / start / end) and delete** on the underlying calendar entry; occasions
  additionally link to their detail page.
- Not in scope (separate change): a database constraint preventing overlapping
  terms of the same article, and adding times to the entries.

## Capabilities

### New Capabilities

- `detail-calendar`: the calendar module in the detail view — the month grid
  with range bars and single-day dots, month scrolling with lazy loading, period
  selection with a conflict check and an action choice, and term preview with
  generic entry edit/delete.

### Modified Capabilities

- `planning`: the article-level mini calendar becomes the detail calendar (grid
  plus list); calendar entries become editable and deletable from the detail
  view.

## Impact

- `hub` templates: `articleCalendar.html` (grid + list + switch) and new
  partials; `header.html` (CSS/JS).
- `article` views: build the calendar items from the article's `CalendarEntry`s
  (and the expiry date); new endpoints for month rendering, the conflict check,
  and generic entry edit/delete.
- `organisation`: a new per-user setting for the calendar/list switch.
- `locales`: new UI strings.

