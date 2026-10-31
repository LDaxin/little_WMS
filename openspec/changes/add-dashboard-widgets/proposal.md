## Why

§24 describes custom dashboard widgets based on saved views (§10): a user can
place a saved view on the dashboard. The dashboard exists; the custom widgets do
not.

## What Changes

- `SavedView.show_on_dashboard` (default off).
- The dashboard renders a widget per own saved view with that flag, listing the
  view's articles (a few) with a link to apply it.
- A toggle on the My Views page.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `dashboard`: custom widgets from saved views.
- `saved-views`: a show-on-dashboard flag.

## Impact

- `savedviews` gains a field; the dashboard view/template render the widgets.
- **Deferred**: drag-and-drop ordering; per-user show/hide beyond the flag.
