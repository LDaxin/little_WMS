## Why

§10 describes share links: a saved view can be shared via a capability URL,
with its own access mode, expiry, single-use, and optional password. Today a
saved view is only visible to logged-in members.

## What Changes

- A `ShareLink` model (saved view, token, access mode, expiry, single-use,
  password, active).
- A "Share" action on a saved view creates a link.
- A public view `/s/<token>/` validates the token (active, not expired, not used
  up), checks the password, and shows the view's articles read-only.
- An "Active Links" overview with revoke.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `saved-views`: share links.

## Impact

- `savedviews` app gains the `ShareLink` model and views.
- **Deferred**: link permissions (reserve / check_out / edit / quantity_change) —
  read-only for now.
