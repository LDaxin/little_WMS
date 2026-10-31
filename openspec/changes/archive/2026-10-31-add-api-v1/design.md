## Context

§7a describes an API-first architecture. DRF is barely wired up; this change
adds a read-only API under `/api/v1/`, reusing the §3 role system for
permissions.

## Goals / Non-Goals

**Goals:**

- A `/api/v1/` router with read-only endpoints for the main models.
- Permissions coupled to the role system.

**Non-Goals:**

- Write operations (CRUD).
- Token / JWT auth.
- OpenAPI (drf-spectacular).
- Wiring the service layer into the API.

## Decisions

### Decision 1: A dedicated `api` app

Serializers, viewsets, permissions, and the router live in one `api` app, so the
domain apps stay free of API concerns.

### Decision 2: Read-only first

`ReadOnlyModelViewSet` for each model. Write operations are a later change, so
the API cannot mutate data yet.

### Decision 3: `RolePermission`

A DRF permission class maps the HTTP method to a role action (`GET`→view,
`POST`→create, `PUT`/`PATCH`→edit, `DELETE`→delete) and the viewset to a
permission area (`permission_area`), checked with `has_perm` against the active
organisation. It is the default permission.

### Decision 4: Session + basic auth

Session auth (the existing login) for the browsable API, basic auth for simple
clients. Token/JWT is deferred.

## Risks / Trade-offs

- [Read-only] → intentional; writes need careful validation and are a later
  change.

## Migration Plan

- None.
