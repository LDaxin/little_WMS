## Why

§30 lists E-Mail / SMTP. Today the system has no email code at all: invitations
are link-only (the link is shown in the UI), notifications are in-app only, and
there are no `EMAIL_*` settings. Several built features (invitations, later
notifications and loan reminders) need a way to actually send mail.

## What Changes

- Env-driven SMTP settings (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`,
  `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`). Without
  `EMAIL_HOST` the system uses the console backend and reports "not configured".
- A central mail service (`hub/mail.py`) that is the single send path. When SMTP
  is not configured it logs a warning and skips instead of failing.
- Invitations: creating an invitation with an email sends the invite link.
- Server settings page: shows the SMTP status and offers a "Send test email"
  button.
- `.env.example` documents the new variables.

## Capabilities

### New Capabilities

- `email`: SMTP configuration from the environment, a central mail service with
  a graceful fallback, and a test-email action.

### Modified Capabilities

- `invitations`: creating an invitation with an email sends the invite link.

## Impact

- `little_wms/settings.py`, a new `hub/mail.py`, `organisation` views/templates,
  `.env.example`.
- **Deferred** (separate changes): email-address verification / double opt-in so
  only confirmed addresses receive mail; loan reminders (§20); notification
  emails (§6); HTML templates and i18n (§14). Password reset already works once
  SMTP is configured (Django built-in).
