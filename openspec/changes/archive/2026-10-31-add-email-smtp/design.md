## Context

§30 lists E-Mail / SMTP. The system currently has no email code. This change
adds the SMTP configuration and the single send path that later features
(verification, notifications, loan reminders) build on.

## Goals / Non-Goals

**Goals:**

- Configure SMTP from the environment (secrets stay out of the DB and git).
- One central mail service as the only place that sends mail.
- Graceful fallback: no SMTP configured → skip + log warning, never crash.
- Send invitation links by email; a "Send test email" action on the server page.

**Non-Goals:**

- Email-address verification / double opt-in (next change).
- Loan reminders (§20), notification emails (§6).
- HTML templates and i18n (§14) — plain text for now.

## Decisions

### Decision 1: Env-driven settings, console backend when unconfigured

`EMAIL_*` come from the environment (like `SECRET_KEY`). When `EMAIL_HOST` is
unset, `EMAIL_BACKEND` falls back to the console backend so development works
without a mail server, and `EMAIL_CONFIGURED` is `False`.

### Decision 2: A single mail service

`hub/mail.py` exposes `send(to, subject, body)`. It is the only place that calls
Django's mail API. When `EMAIL_CONFIGURED` is `False` it logs a warning and
returns `False`. This is the choke point where email-address verification will
later be enforced, so no caller has to know about it.

### Decision 3: Plain-text emails

Invitation and test emails are plain text. HTML templates and translation are
deferred to §14.

## Risks / Trade-offs

- [Sending to unverified addresses] → only explicit actions send mail in this
  change (invitation creation, test email); the verification gate follows in the
  next change.
- [Dev data with real addresses] → the dev database is cleaned of email
  addresses before this is used.

## Migration Plan

- None (no model changes).
