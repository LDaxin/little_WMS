## Why

Approving an organisation request creates the organisation and an invitation for
the requester's email, but the invitation link is never shown. With no SMTP
configured, the requester can never join — the organisation ends up with no
admin who can log in.

## What Changes

- `OrganisationRequest` links to the invitation created on approval.
- The organisation-requests page shows the invitation link for approved requests
  (with a copy button), so the server admin can pass it on.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `organisations`: show the invitation link after approving a request.

## Impact

- `OrganisationRequest.invitation` (FK, nullable) + migration.
- The approve view links the invitation; the requests template shows the link.
