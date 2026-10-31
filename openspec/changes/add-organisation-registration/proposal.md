## Why

§23 describes how new organisations join the server: a registration policy
(open / invite only / request) and, for "request", an organisation request with
a mandatory reason that a server admin approves. Today there is no way to create
a new organisation from the UI.

## What Changes

- A server-level registration policy (`open` / `invite` / `request`).
- A public "register organisation" page that follows the policy:
  - `open` → the organisation and its first admin are created.
  - `request` → an organisation request (name, email, reason) is recorded.
  - `invite` → a message that registration is invite-only.
- A server-admin page to review organisation requests (approve / reject).
- A server-admin page to set the registration policy.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `organisations`: organisation registration and requests.

## Impact

- `hub.Settings` gains `registration_policy`; new `OrganisationRequest` model.
- New views/urls/templates in the `organisation` app.
- **Deferred**: double opt-in (needs SMTP, §30); the user onboarding tour.
