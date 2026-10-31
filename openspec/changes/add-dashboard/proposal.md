## Why

§24 describes the dashboard as the command center: what matters right now,
role-specific. Today the landing page is only a grid of tiles. With occasions,
notifications, and the checks layer in place, a dashboard can surface them.

## What Changes

- A dashboard page with permission-gated widgets: upcoming occasions,
  notifications, alerts (from the checks layer), quick actions, statistics, and
  recent activity.
- A `has_perm` template filter for permission gating in templates.
- A link from the hub.

## Capabilities

### New Capabilities

- `dashboard`: the command center with permission-gated widgets.

### Modified Capabilities

<!-- none -->

## Impact

- New view/url/template in the `hub` app; a template filter in `organisation`.
- **Deferred**: custom widgets from Saved Views (§10); per-user show/hide and
  drag-and-drop ordering.
