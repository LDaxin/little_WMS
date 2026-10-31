## 1. Model

- [x] 1.1 `EmailVerification` model (user, email, verified, token) + migration

## 2. Service

- [x] 2.1 `request_verification(user)` — create/update record, send link
- [x] 2.2 `verify(token)` — mark verified; `is_verified(email)` lookup

## 3. Enforcement

- [x] 3.1 `hub.mail.send(..., require_verified=True)` skips unverified recipients
- [x] 3.2 Invitations send with `require_verified=False`

## 4. Flow

- [x] 4.1 Request verification on registration and invitation accept
- [x] 4.2 Public `/verify-email/<token>/` view + template

## 5. UI

- [x] 5.1 Users page shows status and offers a resend

## 6. Tests

- [x] 6.1 Request on register / invitation accept
- [x] 6.2 Confirm marks verified; unknown token rejected
- [x] 6.3 Mail service skips unverified, sends verified, exempt passes
- [x] 6.4 Resend issues a new token

## 7. Verify

- [x] 7.1 Full test suite green in Docker
- [x] 7.2 Rebuild Docker for manual testing
