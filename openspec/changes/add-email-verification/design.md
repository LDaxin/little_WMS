## Context

§30 added email sending. This change adds double opt-in so only confirmed
addresses receive mail, enforced in the central mail service.

## Goals / Non-Goals

**Goals:**

- A per-user verification record with a token and a `verified` flag.
- Send a confirmation link on registration and invitation accept.
- A public link that marks the address verified.
- The mail service skips unverified recipients; invitations are exempt.

**Non-Goals:**

- Re-verification on email change (no email-edit UI yet).
- Notification emails (§6) and loan reminders (§20) — they will use the gate.
- A third-party dependency (e.g. django-allauth).

## Decisions

### Decision 1: A small `EmailVerification` model

One record per user (`OneToOneField`), holding the address, a `verified` flag,
and a token. A new token is issued on every request. This is the minimum that
supports double opt-in without a custom user model.

### Decision 2: Enforcement in the mail service

`hub.mail.send(to, subject, body, require_verified=True)` skips (and logs) when
the recipient is not verified. Invitations call it with
`require_verified=False`, because they go to people without an account. The
verification lookup is imported lazily to avoid a hub ↔ organisation cycle.

### Decision 3: Verification is per user, matched by address

`is_verified(email)` checks for a verified record with that address. Good enough
for a small WMS; a per-user check would need the caller to pass a user.

## Risks / Trade-offs

- [Existing users are unverified] → they receive no mail until an admin resends
  the confirmation from the users page.
- [Address matched by string] → two users sharing an address share the status;
  acceptable here.

## Migration Plan

- New table only; no data migration.
