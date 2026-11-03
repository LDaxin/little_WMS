## Context

`has_perm(user, perm, organisation)` evaluates a permission against the user's
role. The share view (`shareLinkView`) is public and currently decides the
`borrow` action with `link.can_borrow()` and `request.user.is_authenticated`,
bypassing the permission check entirely. §3 asks for the check to be able to
take permissions from a link context.

## Goals / Non-Goals

**Goals:**

- The permission check can use a share link's permissions instead of the role.
- A logged-in user can switch between the link's permissions and their own role.
- No behaviour change for anonymous visitors (the link is the capability).

**Non-Goals:**

- New link actions (`reserve`, `check_out`, `check_in`, `edit`,
  `quantity_change`) — only the existing `view`/`borrow` are mapped.
- A session-wide "act as link" mode; the toggle applies to the share view.

## Decisions

### Decision 1: `has_perm(..., link=None)`

When `link` is given, the check returns whether the link's action list maps to
the requested codename, ignoring the user's role. This keeps one entry point for
permission checks.

### Decision 2: Link actions map to catalogue codenames

`LINK_ACTIONS = {"view": "article.view_all", "borrow": "article.move_all"}` in
`organisation/permissions.py`, next to the catalogue. `link_codenames` turns a
link's action list into codenames.

### Decision 3: Mode in the session

The share view stores the mode (`link` or `mine`) in the session per link. The
default is `link` (the capability URL is the access). Anonymous visitors always
use the link.

## Risks / Trade-offs

- [Mode drift] → the mode is per link and per session; a new session starts in
  `link` mode.

## Migration Plan

- No schema change; the `permissions` field already exists.
