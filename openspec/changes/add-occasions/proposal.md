## Why

§2 describes the Occasion System: the reason material is needed (a summer camp,
a trip). Today there is no way to plan material for an event — you can only move
articles. Occasions with a packlist are the missing planning layer.

## What Changes

- New models: `CalendarEntry` (base entry with type, title, dates, responsible
  user), `OccasionType`, `Occasion`, `Packlist`.
- Occasions can be created, listed, edited, and deleted.
- A packlist lists the articles an occasion needs, each with a quantity and a
  status (needed/reserved/checked_out/returned).
- Occasion permissions (`occasion.*`) are enforced.
- Hub gets a link to the occasion list.

## Capabilities

### New Capabilities

- `occasions`: plan material for an event with a packlist.

### Modified Capabilities

<!-- none -->

## Impact

- New app or module with models + migration(s).
- Occasion list/detail/CRUD views, packlist editor.
- Navigation: a hub entry.
- **Deferred** (later changes): occasion templates, recurrence, copying, the
  central calendar view (§2), the article-level mini calendar, and resolving the
  `assigned` scope over occasion helpers (see §3 backlog note).
