## Why

An organisation needs a way to add members. Today a membership can only be
created by hand; there is no self-service way to join. Invitations let an admin
invite someone with a pre-set role via a shareable link.

## What Changes

- New `Invitation` model: organisation, optional email, role, token, inviter,
  expiry, accepted_at, status.
- An admin creates an invitation link (optionally emailed) with a role and an
  expiry (default 7 days).
- A visitor opens the link, registers or logs in, and joins the organisation
  with the invited role.
- Invitations can be revoked; expired, accepted, or revoked ones are not usable.

## Capabilities

### New Capabilities

- `invitations`: invite people to an organisation via a link/token with a role.

### Modified Capabilities

<!-- none -->

## Impact

- New model + migration in the `organisation` app.
- New views/URLs to create and accept invitations.
- Roles UI: an "Invite" action.
- No SMTP required — email is optional.
