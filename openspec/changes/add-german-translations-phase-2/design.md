## Context

§14 lists internationalization. Phase 1 translated the core UI. This change
finishes the remaining apps.

## Goals / Non-Goals

**Goals:**

- Wrap and translate the remaining templates and Python strings.
- Extend `locale/de` and recompile.

**Non-Goals:**

- Translating user data (article names, tags, locations).
- New languages.

## Decisions

### Decision 1: Same approach as phase 1

`{% load i18n %}` + `{% trans %}` in templates, `gettext`/`gettext_lazy` in
Python. `makemessages -l de` extracts; the `.po` is extended and compiled.

### Decision 2: Model field names via `verbose_name`

Model fields get `verbose_name=_("...")` so form labels are translated.

## Risks / Trade-offs

- [Large mechanical change] → low risk; tests stay green.

## Migration Plan

- None.
