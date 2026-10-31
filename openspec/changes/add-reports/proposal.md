## Why

§33 describes reporting as the second level beyond the dashboard widgets: a
reports view to dig deeper, filter, and export. Today there is no way to see
activity trends or usage.

## What Changes

- A `reports` app with a `/reports/` view and a time-range filter.
- Reports as tables: movements over time (per month), usage (top articles), and
  user activity.
- A CSV export of the current selection.

## Capabilities

### New Capabilities

- `reports`: activity and usage reports.

### Modified Capabilities

<!-- none -->

## Impact

- New `reports` app; a hub link.
- **Deferred**: diagrams (bar/line); PDF export; the Query Builder filter (§9);
  storage-usage / occasion-history / consumption reports; forecasts.
