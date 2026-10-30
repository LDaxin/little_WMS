## 1. Model

- [x] 1.1 Add `Invitation` model (organisation, email, role, token, invited_by, created_at, expires_at, accepted_at, status)
- [x] 1.2 Add the migration
- [x] 1.3 Add status/validity helpers (pending, expired, accepted, revoked)

## 2. Create and revoke

- [x] 2.1 View + URL to create an invitation (requires `user.invite_all`)
- [x] 2.2 View + URL to revoke a pending invitation
- [x] 2.3 "Invite" action in the roles/users UI

## 3. Accept

- [x] 3.1 Public accept view + URL `/invite/<token>/`
- [x] 3.2 Minimal signup form for anonymous visitors
- [x] 3.3 Create the membership and set the active organisation on accept
- [x] 3.4 Reject expired, accepted, or revoked invitations

## 4. Tests

- [x] 4.1 Model: token uniqueness, expiry, status
- [x] 4.2 Create/revoke views (permission enforced)
- [x] 4.3 Accept as new user, existing user, and already-member
- [x] 4.4 Reject expired, accepted, and revoked invitations

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker for manual testing
