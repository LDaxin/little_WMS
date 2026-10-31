## Context

§10 describes share links. Saved views exist; this change adds capability URLs
for them.

## Goals / Non-Goals

**Goals:**

- A `ShareLink` model and a public view resolving the token.
- Access modes, expiry, single-use, password, revoke.

**Non-Goals:**

- Link permissions (reserve / check_out / edit / quantity_change) — read-only.

## Decisions

### Decision 1: A `ShareLink` model

`saved_view`, `token`, `access_mode`, `expires_at`, `single_use`, `used_count`,
`is_active`, `password_hash`, `created_by`, `created_at` per §10.

### Decision 2: A capability URL

`/s/<token>/` is the access; the link itself is the permission. The view
validates the token, checks the password, and shows the saved view's articles
read-only.

### Decision 3: Password via Django's hashers

`password_hash` uses `make_password`/`check_password`.

### Decision 4: Single use

Opening a single-use link increments `used_count`; once used it is rejected.

## Risks / Trade-offs

- [Read-only] → intentional; write permissions are a later change.

## Migration Plan

- One new model.
