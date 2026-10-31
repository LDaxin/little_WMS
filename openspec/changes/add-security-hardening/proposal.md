## Why

§29 lists security hardening. Django covers CSRF/XSS/SQLi/passwords, but the app
is not HTTPS-capable by configuration and has no login rate limiting.

## What Changes

- HTTPS-capable settings, driven by an env var (`SECURE_HTTPS`): SSL redirect,
  secure cookies, HSTS, proxy header.
- Login rate limiting: a custom login view limiting failed attempts per IP and
  per account, with a temporary lockout and logging.

## Capabilities

### New Capabilities

- `security`: HTTPS-capable settings and login rate limiting.

### Modified Capabilities

<!-- none -->

## Impact

- `little_wms/settings.py`; a new `security` app with the login view.
- **Deferred**: file-upload hardening (no image uploads yet, §15); backup
  encryption (operational); a `django-axes` dependency.
