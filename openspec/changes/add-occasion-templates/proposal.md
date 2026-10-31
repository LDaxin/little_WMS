## Why

§2 describes occasion templates: predefined occasions with a default packlist,
reusable across events ("Standard Summer Camp" with its usual tents, beds, and
kitchen set). Today every occasion's packlist has to be built from scratch, even
when it repeats every year.

## What Changes

- New model `OccasionTemplate` (name, occasion type, default packlist).
- "Save as template" on an occasion captures its type and packlist.
- Creating an occasion can pick a template: the type is pre-filled and the
  packlist is copied.
- A template list page to view and delete templates.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `occasions`: add occasion templates (reusable default packlists).

## Impact

- New model + migration in the `occasion` app.
- New views/urls/templates for the template list and the save/create flows.
- Occasion detail gets a "Save as template" action; the add-occasion form gets a
  template selector.
- **Deferred** (later changes): editing a template's packlist in place (re-save
  from an occasion covers it), recurrence, copying, the central calendar view,
  and the article-level mini calendar.
