## Context

§9 describes a visual query builder. This change adds the parser and a first UI
on the article list.

## Goals / Non-Goals

**Goals:**

- A `QueryParser` (JSON → `Q`) with a field/operator whitelist.
- An advanced builder on the article list.

**Non-Goals:**

- Presets (save/share); drag & drop.
- The other use sites (storage list, QR print, export, packlist, movement
  search, dashboard widgets).

## Decisions

### Decision 1: A `querybuilder` app

The parser is a shared service; a dedicated app keeps it reusable across views.

### Decision 2: Whitelist per model

`ARTICLE_FIELDS` maps allowed fields to a type; `OPERATORS` maps each type to
allowed operators. Unknown fields/operators raise `QueryError`.

### Decision 3: Vanilla JS

The project has no Alpine.js; the builder is plain JS that builds the JSON and
submits it via HTMX to the search view.

### Decision 4: The search view accepts `query`

`searchArticle` applies the parsed query when a `query` parameter is present,
otherwise the existing quick search.

## Risks / Trade-offs

- [Whitelist maintenance] → fields must be added explicitly; safe by default.

## Migration Plan

- None.
