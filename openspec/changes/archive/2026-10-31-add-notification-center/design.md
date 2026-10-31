## Context

§6 describes a notification system. Only transient toasts exist; their text is
built ad hoc in each view. This change adds persistent per-user notifications, a
center, and a single service to create them.

## Goals / Non-Goals

**Goals:**

- A `Notification` model and a central creation service.
- A notification center (bell, dropdown, page, mark-as-read).
- Translation-ready messages (gettext in the service).

**Non-Goals:**

- The triggers (expiry, maintenance, low stock).
- Email / webhook delivery, digests, a rules UI.
- Centralising the toast feedback.

## Decisions

### Decision 1: New `notifications` app

Notifications are a distinct domain; a dedicated app keeps the model, service,
views, and templates together.

### Decision 2: A central service

`notifications/services.py` exposes `notify(user, ...)` and
`notify_roles(organisation, codename, ...)`. Views call the service; they never
build notification text. This is the single place to translate.

### Decision 3: Messages via gettext

The service builds the title/message with `gettext`, so the strings are
translatable. Per-recipient language (key + params, translated at render) is a
later refinement.

### Decision 4: Unread count via a context processor

A context processor exposes the unread count so the header bell can render it on
every page.

### Decision 5: Permission

The notification page requires `notification.view_all` (already in the §3
catalogue).

## Risks / Trade-offs

- [Context processor query per request] → a single indexed count; fine.

## Migration Plan

- New app with an initial migration.
