## Why

§14 lists internationalization. The infrastructure (per-user language, locale
middleware) exists, but the UI is English-only. This change adds German and
translates the core UI.

## What Changes

- Add `("de", "Deutsch")` to `LANGUAGES`.
- Wrap the core UI strings (templates and Python) with `gettext` / `{% trans %}`
  and provide German translations.
- Core UI: navigation, login, hub, dashboard, notifications (center + rules),
  preferences, server settings, the organisation pages (users, roles,
  registration, invitations, verification, configuration), the import pages, and
  the common modules (toasts, search, modals, item forms).

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `i18n`: German is available and the core UI is translated.

## Impact

- `little_wms/settings.py`, the core templates and views, `locale/de/`.
- **Deferred**: the remaining apps (article, storage, movement, occasion,
  planning, loans, reports, saved views, query builder, export, trash,
  onboarding).
