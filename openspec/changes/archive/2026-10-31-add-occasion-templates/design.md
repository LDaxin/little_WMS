## Context

§2 describes occasion templates. The core occasion system (types, occasions,
packlist) exists; this change adds reusable templates on top of it.

## Goals / Non-Goals

**Goals:**

- Store a reusable default packlist per template.
- Save an occasion as a template; create an occasion from a template.
- List and delete templates.

**Non-Goals:**

- Editing a template's packlist in place (re-save from an occasion covers it).
- Recurrence, copying, the central calendar view, the article-level mini calendar.

## Decisions

### Decision 1: `OccasionTemplate` with a JSON default packlist

`OccasionTemplate` — `organisation`, `name`, `occasion_type` (FK),
`default_packlist` (JSON list of `{"article": <pk>, "quantity": <int>}`), using
the `organisation` FK + `SoftDeleteOrganisationManager` pattern of the other
models. A JSON list keeps it to one model and one migration; the packlist is a
small, template-owned snapshot, not a relational entity.

### Decision 2: Save as template captures the current packlist

A POST action on the occasion detail serialises the occasion's packlist into
`default_packlist` and stores the occasion type. No separate editor.

### Decision 3: Create from template on the add-occasion form

The add-occasion form gets an optional template selector. When a template is
chosen, its type is used and its packlist entries are copied onto the new
occasion (unknown/deleted articles are skipped).

### Decision 4: Permissions

Template views reuse the occasion permissions: list → `occasion.view_all`;
save/create-from → `occasion.create_all`; delete → `occasion.delete_all`.

## Risks / Trade-offs

- [Stale article references] → a template's JSON may point at a deleted article;
  creating from a template skips missing articles instead of failing.

## Migration Plan

- One new model with an initial migration. No data migration.

## Open Questions

- Should templates be editable in place? (deferred; re-save from an occasion
  covers the common case)
