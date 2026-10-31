## 1. Settings

- [x] 1.1 Env-driven `EMAIL_*` settings with console fallback and `EMAIL_CONFIGURED`
- [x] 1.2 Document the variables in `.env.example`

## 2. Mail service

- [x] 2.1 `hub/mail.py` `send()` — single send path, skip + warn when unconfigured

## 3. Invitation email

- [x] 3.1 `inviteCreate` sends the invite link when an email is given

## 4. Server settings

- [x] 4.1 Show SMTP status and add a "Send test email" action

## 5. Tests

- [x] 5.1 Mail service skips (and warns) when email is not configured
- [x] 5.2 Invitation with an email sends the link (locmem backend)
- [x] 5.3 Test-email action reports sent / not configured

## 6. Verify

- [x] 6.1 Full test suite green in Docker
- [x] 6.2 Rebuild Docker for manual testing
