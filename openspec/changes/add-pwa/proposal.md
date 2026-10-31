## Why

§34 describes the app as a Progressive Web App: installable ("Add to home
screen") with a cached app shell so it starts without network. Today it is only
a website.

## What Changes

- A `manifest.json` (name, short_name, start_url, standalone display, theme
  color, icons).
- A service worker (`/sw.js`, root scope) caching the app shell and static
  assets.
- The header links the manifest and registers the service worker.

## Capabilities

### New Capabilities

- `pwa`: installable, app-shell-cached web app.

### Modified Capabilities

<!-- none -->

## Impact

- New views/urls in the `hub` app; the header links the manifest and registers
  the service worker.
- **Deferred**: full offline (local DB + sync, explicitly out of scope); the
  scan offline queue (§16.13); PNG icons / splash screens.
