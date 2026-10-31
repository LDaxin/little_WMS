## Context

§29 lists security hardening. Django covers the basics; this change adds
HTTPS-capable settings and login rate limiting.

## Goals / Non-Goals

**Goals:**

- Env-driven HTTPS settings.
- Login rate limiting per IP and per account.

**Non-Goals:**

- File-upload hardening (no image uploads yet).
- Backup encryption (operational).
- A `django-axes` dependency.

## Decisions

### Decision 1: Env-driven HTTPS settings

`SECURE_HTTPS` toggles `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`,
`CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`, and `SECURE_PROXY_SSL_HEADER`, so
local development is unaffected.

### Decision 2: A custom login view

A `security` app provides a login view that counts failed attempts per IP and
per username in the cache, locks out after a threshold, and logs failures. It is
registered before `django.contrib.auth.urls`.

## Risks / Trade-offs

- [Cache-based counters] → reset on restart; acceptable for a small WMS.

## Migration Plan

- None.
