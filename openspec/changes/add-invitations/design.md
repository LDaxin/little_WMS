## Context

Organisations and roles exist (§3, §22), but there is no way to add a member
except by hand. §23 describes registration, invitations, and onboarding; this
change covers the invitation slice plus the minimal signup an invited user
needs. Email sending (§30) and the server registration policy are out of scope.

## Goals / Non-Goals

**Goals:**

- An admin can create an invitation link with a role and an expiry.
- A visitor can accept it (registering if needed) and joins the organisation.
- Invitations are single-use and can be revoked.

**Non-Goals:**

- Sending invitation emails (SMTP, §30).
- The server registration policy (Open / Invite / Request) and
  `OrganisationRequest`.
- The user onboarding tour.
- Self-service organisation creation.

## Decisions

### Decision 1: `Invitation` model in the `organisation` app

Fields: `organisation`, `email` (blank), `role` (nullable), `token` (unique),
`invited_by`, `created_at`, `expires_at`, `accepted_at`, `status`. Kept in the
`organisation` app because it is about membership.

### Decision 2: Token generation

`secrets.token_urlsafe(32)` (~43 chars), stored unique. Single-use: accepting
sets `status=accepted` and `accepted_at`.

### Decision 3: Accept URL and minimal signup

`/invite/<token>/` is public. If the visitor is anonymous, show a minimal signup
(username + password, email optional) or a login link; on success, create the
membership, set the active organisation, and redirect to the hub. A logged-in
user accepts directly. This keeps the change self-contained without pulling in
the full registration policy.

### Decision 4: Permission

Creating and revoking invitations requires `user.invite_all` (already in the
catalogue). Accepting requires no permission.

## Risks / Trade-offs

- [Token leakage] → tokens are single-use and expire (default 7 days).
- [Signup spam] → out of scope here; the registration policy (§23) will gate it.
- [Duplicate membership] → accepting when already a member just marks the
  invitation accepted, no duplicate profile.

## Migration Plan

- Add the `Invitation` model + migration.
- No data migration needed (new table).

## Open Questions

- Should the invited email be enforced (only that email may accept)? Default:
  no, the link is shareable.
