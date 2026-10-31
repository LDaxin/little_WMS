## Context

§20 loans have a return date but no reminder. §6 defines a `return_overdue`
trigger. The notification checks layer already yields findings that the
`check_notifications` command turns into notifications.

## Goals / Non-Goals

**Goals:**

- A `return_overdue` finding for active loans past their return date, in both
  directions (lent out and borrowed in).

**Non-Goals:**

- Per-trigger recipients (Admin + occasion responsible) — configurable rules.
- A separate reminder command or schedule.

## Decisions

### Decision 1: A check in the existing checks layer

`return_overdue_findings(organisation)` yields a finding per overdue loan, with
a stable `dedupe_key` so the existing dedupe prevents repeats. It is added to
`CHECKS`, so `check_notifications` picks it up with no other change.

### Decision 2: Both directions

A `Lending` (lent out) is overdue when active and its `loan` calendar entry's
end date has passed. A `Loan` (borrowed in) is overdue when active and its end
date has passed.

## Risks / Trade-offs

- [Recipients are the existing `article_view_all` role] → the occasion
  responsible is not notified yet; that needs the configurable rules.

## Migration Plan

- None.
