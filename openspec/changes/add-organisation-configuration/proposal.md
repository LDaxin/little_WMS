## Why

§8 describes standard configurations and onboarding: an organisation needs
article types, storage types, and role templates before it can be used. Today
there is no UI to create article types or storage types, so a new organisation
cannot be set up.

## What Changes

- A configuration page for the organisation admin that lists and creates article
  types and storage types.
- A "load defaults" action that creates the standard types from §8.
- A "create role templates" action that creates the standard role templates.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `organisations`: organisation configuration (article types, storage types,
  role templates).

## Impact

- New views/urls/template in the `organisation` app.
- **Deferred**: the multi-step onboarding wizard; a custom-fields editor for
  article types; a `setup_defaults` management command.
