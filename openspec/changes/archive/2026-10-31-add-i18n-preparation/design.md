## Context

§14 lists internationalization. The app is English-only; only the notification
checks use `gettext`. This change prepares the infrastructure without adding a
second language yet.

## Goals / Non-Goals

**Goals:**

- `LANGUAGES`, `LOCALE_PATHS`, `LocaleMiddleware`.
- A per-user `UserProfile.language` (default English) and a middleware that
  activates it.
- A language selector on the preferences page.
- Import strings wrapped for translation.

**Non-Goals:**

- German translations, translating the rest of the UI.
- Organisation-level language, onboarding language, timezone levels.

## Decisions

### Decision 1: Only English for now

`LANGUAGES = [("en", "English")]`. Adding a language later means adding it to
`LANGUAGES` and providing a `.po` file — no code change.

### Decision 2: Language from the user profile

A `UserLanguageMiddleware` (after `LocaleMiddleware` and
`AuthenticationMiddleware`) activates the profile's language, so the setting
wins over the browser's `Accept-Language`.

### Decision 3: Wrap the import strings

The import service and templates use `gettext` / `{% trans %}` so they are ready
to translate; the rest of the UI follows incrementally.

## Risks / Trade-offs

- [Profile lookup per request] → one extra query; acceptable for a small WMS.
- [Partial wrapping] → only the import is wrapped; the rest stays literal until
  translated.

## Migration Plan

- New `UserProfile.language` column with a default; no data migration.
