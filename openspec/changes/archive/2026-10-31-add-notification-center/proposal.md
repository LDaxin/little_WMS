## Why

§6 describes a notification system with an in-app notification center. Today the
only "notifications" are transient Bootstrap toasts, whose text and context are
built ad hoc in every view. There is no persistent, per-user notification, no
center to review them, and no single place to translate the texts.

## What Changes

- New `notifications` app with a `Notification` model (per user).
- A central `services.notify` / `notify_roles` API, so views never build
  notification text themselves; messages are produced via gettext.
- A notification center: a bell with an unread badge, a dropdown with the latest
  five, and a page listing all notifications with mark-as-read.

## Capabilities

### New Capabilities

- `notifications`: per-user in-app notifications and their center.

### Modified Capabilities

<!-- none -->

## Impact

- New Django app `notifications`; a bell in the header; a context processor for
  the unread count.
- **Deferred**: the triggers themselves (expiry, maintenance, low stock), email
  and webhook delivery, digests, a configurable rules UI; centralising the toast
  feedback.
