## Why

§14 lists internationalization. Phase 1 translated the core UI; the remaining
apps are still English.

## What Changes

- Wrap and translate the remaining templates: article, storage, movement,
  occasion, planning, loans, reports, saved views, query builder, export,
  onboarding, and the remaining hub modules.
- Wrap the remaining Python strings (view toasts/messages, form labels, model
  field names and choices).
- Extend `locale/de` and recompile.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `i18n`: the remaining UI is translated to German.

## Impact

- The remaining templates and views/forms/models, `locale/de`.
