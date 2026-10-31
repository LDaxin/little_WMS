## Context

§6 lists notification triggers. The notification center exists; this change adds
the triggers that fill it, kept separate from the notification delivery.

## Goals / Non-Goals

**Goals:**

- A checks layer producing findings, independent of notifications.
- A command turning findings into notifications.
- Dedupe so the same alert is not repeated.

**Non-Goals:**

- Email / webhook delivery, digests, a rules UI.
- Scheduling (cron is an operational concern).

## Decisions

### Decision 1: Findings are a separate layer

`notifications/checks.py` yields `Finding`s (trigger_type, title, message, link,
dedupe_key). It knows *what* is due, not that a notification results. Other
consumers (email, webhook, dashboard) can reuse the same findings later.

### Decision 2: The command is the notification consumer

`check_notifications` runs the checks per organisation and calls the central
service. It is the only place that maps findings to notifications.

### Decision 3: Dedupe by key

`Notification.dedupe_key` (nullable). The service skips creating a notification
when an unread one with the same key already exists for the user.

### Decision 4: Recipients

Findings go to everyone holding `article.view_all` in the organisation
(`notify_roles`).

## Risks / Trade-offs

- [Checks run per organisation] → fine for a small WMS.

## Migration Plan

- One nullable field on `Notification`.
