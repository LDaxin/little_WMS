## Context

§2 lists maintenance as a calendar entry type linked to an article. The
`planning` app owns `CalendarEntry`; the article detail renders the mini
calendar.

## Goals / Non-Goals

**Goals:**

- Record a maintenance due date for an article.
- Show it in the article mini calendar and the calendar.

**Non-Goals:**

- Generating maintenance from the article type's maintenance interval.
- The `maintenance_due` notification (§6).
- A "done" state.

## Decisions

### Decision 1: `CalendarEntry.article` (nullable FK)

A maintenance entry is a `CalendarEntry` of type "maintenance" with an optional
`article` link. This keeps one entry model and lets the calendar show it like any
other entry; other entry types simply leave `article` empty.

### Decision 2: Add from the article detail

The "Add maintenance" form lives on the article detail (title + due date) and
creates the entry with `article` set.

### Decision 3: Permission

Adding maintenance requires `article.edit_all`.

## Risks / Trade-offs

- [Generic entry gains an article link] → acceptable; it is nullable and only
  used by maintenance for now.

## Migration Plan

- One nullable FK on `CalendarEntry`.
