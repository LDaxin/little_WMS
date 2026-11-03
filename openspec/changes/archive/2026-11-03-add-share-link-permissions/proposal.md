## Why

§3/§10: a share link is a capability URL whose permissions are a *second,
independent permission source* — they replace the user's role for the objects in
the saved view. Today the share view only hard-codes a `borrow` check and the
permission check cannot take permissions from a link context. A logged-in user
also cannot choose between their own permissions and the link's.

## What Changes

- The permission check (`has_perm`) accepts an optional link context: when given,
  the link's permissions are used instead of the role.
- A mapping from link actions (`view`, `borrow`) to catalogue codenames.
- The share view resolves the effective source: anonymous visitors use the link;
  a logged-in user can switch between the link's permissions and their own role.
- A toggle in the share view (logged-in only) switches the mode.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `saved-views`: a share link's permissions can be used as the effective
  permission source, and a logged-in user can switch to their own role.

## Impact

- `organisation` app: permission check + link-action mapping.
- `savedviews` app: model helper, share view, mode view, URL, template.
