## Context

§8 lists Container and Vehicle as storage types, contradicting its own
"movable = article" philosophy.

## Goals / Non-Goals

**Goals:**

- Container and Vehicle become standard article types (with
  `article_toggle_space`).

**Non-Goals:**

- Migrating existing data (the defaults are only suggestions; `ki` is not live).

## Decisions

### Decision 1: Article types with `article_toggle_space`

Both are movable and can hold other articles, so they are article types with
`article_toggle_space = True` (like Box/Crate).

### Decision 2: Update the Lastenheft

§8's tables move Container and Vehicle to the article types.

## Risks / Trade-offs

- [Existing orgs keep their types] → the defaults are suggestions; nothing is
  deleted.

## Migration Plan

- None (constants + docs).
