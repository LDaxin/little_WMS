## Context

`require_perm(perm)` checks an exact codename (`_all` only). To honour the
`assigned` scope we need an assignment field and a scope-aware check. This
change covers articles; storage and occasion follow the same pattern later.

## Goals / Non-Goals

**Goals:**

- Articles can be assigned to users.
- `_all` grants an action; `_assigned` grants it only for assigned articles.
- Lists show only assigned articles for `_assigned`-only users.

**Non-Goals:**

- `assigned` scope for storage and occasion.
- Assignment rules (who may assign) beyond the article `edit` permission.

## Decisions

### Decision 1: `Article.assigned_to` (M2M to auth.User)

`assigned_to = models.ManyToManyField("auth.User", blank=True, related_name="assigned_articles")`.

### Decision 2: Scope helpers in `permissions.py`

- `has_scope(user, area, action, organisation=None, obj=None)`:
  `_all` → True; `_assigned` → True when `obj is None` (list/aggregate) or the
  article is assigned to the user.
- `is_assigned_only(user, area, action, organisation=None)`: the user has
  `_assigned` but not `_all` — used to filter querysets.

### Decision 3: `require_scope(area, action)` decorator

Like `require_perm`, but passes for `_all` **or** `_assigned`. The article views
switch from `require_perm("article.*_all")` to `require_scope("article", "*")`.

### Decision 4: Object-level checks in detail/edit/delete/move

The decorator only knows `obj=None`, so the detail/update/delete/move views
re-check the fetched article with `has_scope(..., obj=article)` and return 403
when a purely `_assigned` user is not assigned.

### Decision 5: List/search/export filtering

When `is_assigned_only(user, "article", "view", org)`, filter the queryset with
`assigned_to=request.user`.

### Decision 6: Assignment UI on the article detail

An "Assigned to" section on the article detail: a user select + add, and chips
with a remove action (like tags). Assigning requires `article.edit` scope on the
article.

## Risks / Trade-offs

- [More permission surface] → covered by dedicated tests.
- [Filtering misses a path] → list, search and export are all filtered.

## Migration Plan

- Add `assigned_to` to `Article` + migration. No data migration.

## Open Questions

- Should the `warehouse`-style templates include `_assigned` examples? (later)
