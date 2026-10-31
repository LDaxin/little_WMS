## Why

§20 loans exist, but nothing reminds anyone when a loan is overdue. §6 lists a
`return_overdue` trigger. With the notification and email system in place, the
reminder is a small addition that completes the loans feature.

## What Changes

- A `return_overdue` check that finds active loans whose return date has passed,
  in both directions (articles lent out and articles borrowed in).
- The check is added to the notification checks, so `check_notifications` turns
  it into notifications (and emails, subject to verification and opt-out).

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `notifications`: a new `return_overdue` trigger for overdue loans.

## Impact

- `notifications/checks.py` (new check), tests.
- **Deferred**: per-trigger recipients (Admin + occasion responsible) — part of
  the configurable notification rules.
