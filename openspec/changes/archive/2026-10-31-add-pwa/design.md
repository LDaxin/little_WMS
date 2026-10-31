## Context

§34 describes the PWA. The app is a Django site; this change adds the manifest,
a service worker, and the header wiring.

## Goals / Non-Goals

**Goals:**

- A manifest and a service worker caching the app shell + static assets.
- Installable and startable offline (shell only).

**Non-Goals:**

- Full offline (local DB + sync) — explicitly out of scope.
- The scan offline queue (§16.13).
- PNG icons / splash screens.

## Decisions

### Decision 1: Manifest and SW served from the root

`/manifest.json` and `/sw.js` are views in the `hub` app, so the service worker
controls the whole app scope (`/`) and `start_url` is `/`.

### Decision 2: Cache-first for the shell and assets

The service worker caches `/` and the static assets, falling back to the cache
when offline. Data requests still need the server.

### Decision 3: SVG icon

The manifest uses the existing `Logo.svg`, avoiding new PNG assets.

## Risks / Trade-offs

- [Cached shell may go stale] → the cache name is versioned; bump it on release.

## Migration Plan

- None.
