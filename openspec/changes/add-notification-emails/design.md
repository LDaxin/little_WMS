## Context

§6 notifications are in-app only. §30 added a mail service with double opt-in.
This change adds the email channel with a per-category opt-out.

## Goals / Non-Goals

**Goals:**

- A per-user, per-category email preference (opt-out, default subscribed).
- The mail service skips a category the recipient opted out of.
- Notifications and invitations send email; verification/test stay non-optional.
- A page to manage the preferences.

**Non-Goals:**

- Configurable notification rules, digests, webhooks, editable templates.
- Per-organisation preferences (preferences are per user).

## Decisions

### Decision 1: A generic `EmailPreference` row per (user, category)

`EmailPreference(user, category, subscribed=True)`, unique on (user, category).
A missing row means subscribed, so the default is opt-out and new categories
need no data migration.

### Decision 2: Enforcement in the mail service

`hub.mail.send(..., category=None)` looks up the recipient by address; if a user
with that address opted out of the category, the message is skipped and logged.
Non-users (invitations to people without an account) are unaffected.

### Decision 3: Categories as a small fixed list

`notifications` and `invitations` for now; the list is easy to extend.

## Risks / Trade-offs

- [Address matched by string] → same as the verification gate; acceptable here.
- [Instant emails can be noisy] → digests are a later change.

## Migration Plan

- New table only; no data migration.
