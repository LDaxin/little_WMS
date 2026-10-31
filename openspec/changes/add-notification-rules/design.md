## Context

§6 lists configurable notifications. The checks layer yields findings; the
`check_notifications` command turns them into notifications for a hardcoded
role. This change makes the recipients, threshold, and channels configurable.

## Goals / Non-Goals

**Goals:**

- A `NotificationRule` per organisation and trigger type.
- Recipients from roles and individual users; in-app and email channels.
- A rules CRUD page.
- Backward compatible: no rule → the current default.

**Non-Goals:**

- `notify_responsible`, digests, webhooks, editable email templates.

## Decisions

### Decision 1: One rule per trigger, multiple allowed

Rules are matched by `trigger_type`; several active rules for the same trigger
are all applied. A missing rule falls back to the default, so existing
installations keep working.

### Decision 2: Channels split in-app and email

`notify()` gains an `email` flag. A rule with `channel_in_app` creates the
in-app notification; `channel_email` sends the email. Email-only rules send
without an in-app notification.

### Decision 3: Threshold per rule

`threshold_days` is passed to the checks (e.g. the expiry window). The checks
keep their default when no rule sets it.

## Risks / Trade-offs

- [Recipient resolution per finding] → a few queries per finding; fine for a
  small WMS.
- [No rule seeding] → the default applies until an admin creates rules.

## Migration Plan

- New table only; no data migration.
