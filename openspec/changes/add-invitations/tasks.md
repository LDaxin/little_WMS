## 1. Model

- [ ] 1.1 Add `Invitation` model (organisation, email, role, token, invited_by, created_at, expires_at, accepted_at, status)
- [ ] 1.2 Add the migration
- [ ] 1.3 Add status/validity helpers (pending, expired, accepted, revoked)

## 2. Create and revoke

- [ ] 2.1 View + URL to create an invitation (requires `user.invite_all`)
- [ ] 2.2 View + URL to revoke a pending invitation
- [ ] 2.3 "Invite" action in the roles/users UI

## 3. Accept

- [ ] 3.1 Public accept view + URL `/invite/<token>/`
- [ ] 3.2 Minimal signup form for anonymous visitors
- [ ] 3.3 Create the membership and set the active organisation on accept
- [ ] 3.4 Reject expired, accepted, or revoked invitations

## 4. Tests

- [ ] 4.1 Model: token uniqueness, expiry, status
- [ ] 4.2 Create/revoke views (permission enforced)
- [ ] 4.3 Accept as new user, existing user, and already-member
- [ ] 4.4 Reject expired, accepted, and revoked invitations

## 5. Verify

- [ ] 5.1 Full test suite green in Docker
- [ ] 5.2 Rebuild Docker for manual testing
