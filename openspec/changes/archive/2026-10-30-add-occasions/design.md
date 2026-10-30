## Context

§2 describes the occasion system. Nothing exists yet. This change builds the
core (types, occasions, packlist); the calendar view, templates, recurrence, and
the `assigned`-over-occasions resolution are deferred to later changes.

## Goals / Non-Goals

**Goals:**

- Model and manage occasions with a packlist.
- Occasion permissions enforced.

**Non-Goals:**

- Occasion templates, recurrence, copying.
- The central calendar view and the article-level mini calendar.
- Reserving/checking out via the packlist (status is tracked only).
- Resolving the `assigned` scope over occasion helpers (see §3 backlog note).

## Decisions

### Decision 1: New Django app `occasion`

Occasions are a distinct domain; keep them in their own app (models, views,
urls, templates), added to `INSTALLED_APPS` after `movement`.

### Decision 2: Models (per §2)

- `CalendarEntry` — `entry_type` (occasion/maintenance/…), `title`,
  `start_date`, `end_date`, `notes`, `responsible_user`, `organisation`.
- `OccasionType` — `name`, `symbol`, `custom_fields_schema`, `organisation`.
- `Occasion` — `calendar_entry` (OneToOne), `occasion_type`, `location`,
  `participant_count`, `attributes`, `organisation`.
- `Packlist` — `occasion` (FK), `article` (FK), `quantity`, `status`
  (needed/reserved/checked_out/returned).

All use the `organisation` FK + `SoftDeleteOrganisationManager` pattern of the
other apps.

### Decision 3: Permissions

Views are guarded with `require_perm`/`require_scope` on the `occasion` area:
list/detail → `occasion.view_all`; add → `occasion.create_all`;
edit → `occasion.edit_all`; delete → `occasion.delete_all`; packlist →
`occasion.manage_packlist_all`.

### Decision 4: Packlist editor on the occasion detail

Add an article (by code/name) with a quantity; change status; remove. Rendered
with HTMX, like the composition editor.

### Decision 5: Navigation

Add an "Occasions" card/link to the hub.

## Risks / Trade-offs

- [Big change] → split into core (this) + follow-ups; each reviewable.
- [Packlist vs. reservation] → status is informational here; real
  reserve/check-out comes with §20 Loans.

## Migration Plan

- New app with an initial migration. No data migration.

## Open Questions

- Should the occasion list be the future calendar view, or a plain list for now?
  (plain list now; calendar later)
