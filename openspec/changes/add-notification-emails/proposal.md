## Why

§6 lists the notification system. Notifications are in-app only; the email
channel is missing. Now that §30 provides a mail service and double opt-in, the
email channel can be added — with a per-category opt-out so users who do not
want email are not contacted.

## What Changes

- A per-user, per-category email preference (`notifications`, `invitations`),
  default subscribed (opt-out model).
- The central mail service skips a category the recipient has opted out of.
- Notifications send an email (category `notifications`); invitations send with
  category `invitations`. Verification and test emails stay non-optional.
- A preferences page where a user toggles each category.

## Capabilities

### New Capabilities

- `email-preferences`: per-user, per-category opt-out for email.

### Modified Capabilities

- `notifications`: creating a notification also sends an email.
- `email`: the mail service honours the recipient's category preference.

## Impact

- New `EmailPreference` model in `hub` (+ migration), `hub/mail.py`,
  `notifications/services.py`, `organisation` invitation view, a preferences
  page.
- **Deferred**: configurable notification rules, digests, webhooks, editable
  templates.
