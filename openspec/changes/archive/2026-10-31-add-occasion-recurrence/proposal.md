## Why

§2 describes recurring occasions ("Annual summer camp" every year). Recurrence is
a **calendar** concept, not an occasion concept: maintenance, purchases, and
other calendar entries will recur too. Anchoring the rule on the occasion would
force a refactor later.

## What Changes

- New `planning` app holding `CalendarEntry` (moved out of `occasion`) and the
  new `RecurrenceRule`. (Named `planning`, not `calendar`, because a Django app
  named `calendar` would shadow the stdlib module Django itself imports.)
- `CalendarEntry` gains an optional `recurrence_rule`.
- A recurrence rule generates future calendar entries; for occasion entries the
  matching `Occasion` (and its packlist) is created too.
- An occasion can be made recurring from its detail page; the future occasions
  are generated with the packlist copied from the head.

## Capabilities

### New Capabilities

- `planning`: dated calendar entries and recurrence rules.

### Modified Capabilities

- `occasions`: an occasion can be made recurring.

## Impact

- New Django app `planning`; `CalendarEntry` moves from `occasion` to `planning`.
- `ki` is not live, so the model move uses a plain drop/recreate migration and
  the dev database is reset (see `Agents.md`).
- **Deferred**: editing a whole series vs. a single instance; weekday /
  day-of-month selection (taken from the start date); lazy generation (eager,
  bounded by a horizon for "never").
