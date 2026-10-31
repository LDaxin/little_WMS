## Why

§14 lists internationalization. The app is English-only and has no language
setting; only the notification checks already use `gettext`. This change
prepares the language infrastructure so a second language can be added later,
while the app stays English for now.

## What Changes

- `LANGUAGES`, `LOCALE_PATHS`, and `LocaleMiddleware` in the settings.
- A per-user `UserProfile.language` (default English) and a middleware that
  activates it.
- A language selector on the preferences page.
- The import strings are wrapped with `gettext` / `{% trans %}` so they are
  ready for translation.

## Capabilities

### New Capabilities

- `i18n`: per-user language setting and the translation infrastructure.

### Modified Capabilities

<!-- none -->

## Impact

- `little_wms/settings.py`, `organisation` (model, middleware, migration),
  the preferences page, the import strings.
- **Deferred**: German translations (`.po` files), translating the rest of the
  UI, organisation-level language, onboarding language, timezone levels.
