## Why

§2 describes the calendar as the central planning view: everything dated in one
place. The `planning` app already stores `CalendarEntry` (occasions and, later,
maintenance/purchase/…), but there is no view to see them.

## What Changes

- A calendar view listing all calendar entries of the active organisation,
  grouped by month, with the entry type, title, and dates.
- Occasion entries link to their detail page.
- A hub tile linking to the calendar.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `planning`: add the calendar view.

## Impact

- New views/urls/template in the `planning` app.
- A hub tile.
- **Deferred**: the article-level mini calendar; month navigation / filters; a
  month-grid layout.
