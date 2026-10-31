## Context

§2 describes recurring occasions. Recurrence is a calendar concept (maintenance
and other entries will recur too), so the rule is anchored on `CalendarEntry`,
not on `Occasion`. `CalendarEntry` currently lives in the `occasion` app; this
change moves it to a new `calendar` app.

## Goals / Non-Goals

**Goals:**

- A `planning` app owning `CalendarEntry` and `RecurrenceRule`.
- Generate future entries for a rule; occasions get their occasion + packlist.
- Make an occasion recurring from its detail page.

**Non-Goals:**

- Editing a whole series vs. a single instance.
- Weekday / day-of-month selection (taken from the start date).
- Lazy generation (eager, bounded by a horizon for "never").
- The calendar view itself (a later change).

## Decisions

### Decision 1: New `planning` app

`CalendarEntry` moves from `occasion` to `planning`; `RecurrenceRule` lives
there too. The app is named `planning` (not `calendar`) because a Django app
named `calendar` would shadow the stdlib module that `django.utils.dateformat`
imports. Since `ki` is not live (see `Agents.md`), the move uses a plain
drop/recreate migration and the dev database is reset — no data-preserving
migration.

### Decision 2: `RecurrenceRule` on `CalendarEntry`

`CalendarEntry.recurrence_rule` (FK, nullable). Any entry type can recur; the
generation is entry-type-aware.

### Decision 3: Date stepping without a dependency

No `dateutil` in the project. A small helper steps daily/weekly/monthly/yearly,
clamping the day to the month's last day (so Jan 31 + 1 month = Feb 28/29).

### Decision 4: Eager generation, bounded

Applying a rule generates the future entries immediately. The series is bounded
by `end_date` or `end_after_occurrences` (counting the head); with neither, a
2-year horizon is used so "never" cannot generate infinitely.

### Decision 5: Occasion instances copy the head's packlist

For occasion entries, each generated instance gets an `Occasion` (same type,
location, participant count) and a copy of the head's packlist.

### Decision 6: Permissions

Making an occasion recurring requires `occasion.edit_all`.

## Risks / Trade-offs

- [Model move] → drop/recreate; dev DB reset (acceptable, `ki` is not live).
- [Eager generation] → a "never" rule only covers the horizon; a later change
  can extend it lazily.

## Migration Plan

- New `planning` app with an initial migration; `occasion` gets a migration that
  removes `CalendarEntry` and repoints `Occasion.calendar_entry`.
- Dev DB reset + `seed_demo`.

## Open Questions

- Should the horizon be configurable? (constant for now)
