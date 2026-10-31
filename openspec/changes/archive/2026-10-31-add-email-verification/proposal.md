## Why

§30 introduced email sending. To avoid mailing addresses that were never
confirmed, the system should only send to verified addresses (double opt-in).
The dev database held unconfirmed addresses, so this is needed before email is
used for anything beyond explicit invitations.

## What Changes

- A per-user email verification record with a token and a `verified` flag.
- A verification email with a confirmation link, sent on registration and when
  an invitation is accepted (new user).
- A public confirmation link that marks the address verified.
- The central mail service only sends to verified addresses; invitations are
  exempt (they go to people without an account yet).
- The users page shows the verification status and offers a resend.

## Capabilities

### New Capabilities

- `email-verification`: per-user email confirmation (double opt-in) and the
  rule that only verified addresses receive mail.

### Modified Capabilities

- `email`: the central mail service skips unverified recipients unless the
  message is explicitly exempt (invitations).

## Impact

- New `EmailVerification` model in `organisation` (+ migration), a verification
  service, a public verify view/url/template, hooks in registration and
  invitation accept, `hub/mail.py`, the users page.
- **Deferred**: re-verification on email change (no email-edit UI yet);
  notification emails (§6) and loan reminders (§20) that will use the gate.
