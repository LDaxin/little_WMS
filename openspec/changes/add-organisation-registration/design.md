## Context

§23 describes how new organisations join the server. Invitations (joining an
existing organisation) are built; this change adds the organisation-level
registration.

## Goals / Non-Goals

**Goals:**

- A registration policy (open / invite / request).
- A public registration page following the policy.
- Organisation requests with a server-admin review.

**Non-Goals:**

- Double opt-in (needs SMTP, §30).
- The user onboarding tour.

## Decisions

### Decision 1: Policy on `hub.Settings`

`hub.Settings` is the existing server-level singleton (it already holds
`storageDepth`); `registration_policy` lives there.

### Decision 2: `OrganisationRequest` model

`name`, `email`, `reason` (mandatory), `status` (pending/approved/rejected),
`reviewed_by`, `reviewed_at`, `created_at` — per §23.

### Decision 3: Server admin = superuser

The review and settings pages require `is_superuser` (there is no separate
server-admin role yet).

### Decision 4: Open registration creates the first admin

With `open`, the form takes the organisation name and the first admin's
username/email/password; the organisation, a role with all permissions, the
user, and the membership are created, and the user is logged in.

### Decision 5: Approving creates the organisation

Approving a request creates the organisation (slug from the name) and an
invitation for the requester's email, so they can join.

## Risks / Trade-offs

- [Open registration is security-sensitive] → it is off by default (`invite`).

## Migration Plan

- One field on `hub.Settings`; one new model.
