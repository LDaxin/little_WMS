## Why

§8 describes an onboarding wizard: on first start, a guided setup helps
configure the system (article types, storage types, role templates). Today the
configuration page exists, but there is no guided first-run flow.

## What Changes

- `hub.Settings.onboarding_completed` (a flag).
- An `/onboarding/` wizard: questions (usage, context, team size) and the
  suggested article types, storage types, and role templates (pre-selected);
  "Create" applies the selection, "Skip" just marks it done.
- A "restart" link from the configuration page.

## Capabilities

### New Capabilities

- `onboarding`: a first-run setup wizard.

### Modified Capabilities

<!-- none -->

## Impact

- `hub` gains the flag and the wizard view/template.
- **Deferred**: real multi-step navigation; a `setup_defaults` management command
  with profiles; the `ONBOARDING_SKIP` env var.
