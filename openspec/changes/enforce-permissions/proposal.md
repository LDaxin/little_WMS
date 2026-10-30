## Why

The permission catalogue and roles exist (§3), but only the roles/users pages
are actually protected — every other view is reachable by any logged-in user.
Enforcement must be applied consistently so roles mean something.

## What Changes

- Add a permission decorator and apply it to every view of the app.
- Each view is guarded by the matching catalogue permission
  (`article.view_all`, `storage.edit_all`, `article.move_all`, `export.qr_sheet_all`, …).
- Missing permission → 403; superusers pass everything.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `roles-permissions`: add the requirement that every view is protected by its
  permission.

## Impact

- `organisation/decorators.py`: add the decorator(s).
- Every view module: `hub`, `article`, `storage`, `tag`, `location`,
  `codeSystem`, `export`, `movement`, `inventory`.
- No model or migration changes.
