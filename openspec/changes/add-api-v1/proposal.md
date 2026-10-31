## Why

§7a describes an API-first architecture: a complete REST API so a PWA, native
app, or external integration can reuse the same logic. Today DRF is barely
wired up (one broken serializer, no settings, no endpoints).

## What Changes

- A new `api` app with a `/api/v1/` router.
- Read-only serializers and viewsets for the main models (articles, storages,
  locations, tags, spaces, occasions, notifications).
- A `RolePermission` that maps the HTTP method to a role action and the viewset
  to a permission area, reusing the §3 role system.
- DRF settings: session + basic auth, `RolePermission` as the default.

## Capabilities

### New Capabilities

- `api`: a read-only REST API under `/api/v1/`.

### Modified Capabilities

<!-- none -->

## Impact

- New Django app `api`; `REST_FRAMEWORK` settings; the broken
  `article/serializer.py` is removed.
- **Deferred**: write operations (CRUD), token/JWT auth, OpenAPI
  (drf-spectacular), and wiring the service layer into the API.
