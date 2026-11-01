## Why

§12 lists mobile & navigation. The app uses a top navbar that is cramped on
phones and does not adapt to touch. A vertical sidebar works better on mobile
and desktop.

## What Changes

- Replace the top navbar with a vertical sidebar: logo, quick navigation
  (dashboard, articles, storages, movement), notifications, settings, roles,
  logout, and the organisation switcher.
- Responsive CSS: a narrow icon rail that expands on hover (desktop) or via a
  toggle (mobile); the content is padded so the sidebar never covers it.
- Per-user settings: sidebar position (left/right), icon size, text size, and
  view mode (auto / always mobile / always desktop).

## Capabilities

### New Capabilities

- `navigation`: a responsive sidebar replacing the top navbar, with per-user
  position and view-mode settings.

### Modified Capabilities

<!-- none -->

## Impact

- `hub/templates/hub/header.html`, a stylesheet, `UserProfile` (two fields +
  migration), the preferences page, tests.
- **Deferred**: auto-tracked most-used quick navigation, per-view context
  actions.
