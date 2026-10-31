## Context

§2 describes copying occasions. The occasion system (types, occasions, packlist,
templates, recurrence) exists; this adds a duplicate action.

## Goals / Non-Goals

**Goals:**

- Duplicate an occasion with its type, location, participants, and packlist.
- Optionally shift the dates by N days.

**Non-Goals:**

- An empty date (the start date is required; the user edits the copy).
- Copying a whole recurrence series.

## Decisions

### Decision 1: A shift field, not a new date field

The duplicate form takes an optional "shift days" (default 0). This covers the
§2 example ("this year's dates + 364 days") and keeps the start date required;
the user can edit the copy's date afterwards.

### Decision 2: Title

The copy's title is the original plus " (copy)", so the two are distinguishable
in the calendar and lists.

### Decision 3: Permission

Duplicating requires `occasion.create_all`.

## Risks / Trade-offs

- [Same dates when shift is 0] → acceptable; the user edits the copy.

## Migration Plan

- None.
