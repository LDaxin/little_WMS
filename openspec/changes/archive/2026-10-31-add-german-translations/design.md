## Context

§14 lists internationalization. The infrastructure exists (per-user language,
locale middleware, English only). This change adds German and translates the
core UI.

## Goals / Non-Goals

**Goals:**

- `("de", "Deutsch")` in `LANGUAGES`.
- The core UI wrapped and translated to German.

**Non-Goals:**

- The remaining apps (article, storage, movement, occasion, planning, loans,
  reports, saved views, query builder, export, trash, onboarding).
- Translating user data (article names, tags, locations).

## Decisions

### Decision 1: Wrap with `gettext` / `{% trans %}`

Templates use `{% load i18n %}` and `{% trans %}`; Python uses
`gettext`/`gettext_lazy`. `makemessages -l de` extracts them; the `.po` is
translated and compiled.

### Decision 2: Core UI first

The most-used pages and the shared modules are translated first, so the main
workflows are German. The rest follows in a later change.

### Decision 3: English stays the source language

`LANGUAGE_CODE` stays `en-us`; German is a translation. Untranslated strings
fall back to English.

## Risks / Trade-offs

- [Partial translation] → some pages stay English until phase 2; acceptable.
- [`.po` maintenance] → new strings need `makemessages` again.

## Migration Plan

- None.
