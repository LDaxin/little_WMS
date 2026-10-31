## Why

§2 lists maintenance as a calendar entry type ("Tent 'Jurte 8P' – maintenance
due"). The calendar and the article mini calendar already exist, but there is no
way to record a maintenance due date for an article.

## What Changes

- `CalendarEntry` gains an optional `article` link.
- The article detail gets an "Add maintenance" form (title + due date) that
  creates a maintenance calendar entry for the article.
- The article mini calendar shows the article's maintenance entries.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `planning`: maintenance entries linked to an article.

## Impact

- `CalendarEntry.article` (FK, nullable) + migration.
- New view/url in the `article` app; a form on the article detail; the mini
  calendar lists maintenance entries.
- **Deferred**: generating maintenance from the article type's maintenance
  interval; the `maintenance_due` notification (§6); a "done" state.
