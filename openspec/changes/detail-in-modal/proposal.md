## Why

Opening an item today leaves the list: the table's edit button and the cards
navigate to a full detail page. The user wants the detail to open **in a modal**
on the list, so context (filters, scroll, the list itself) is not lost.

## What Changes

- The list's detail trigger (table edit button, cards) opens the entity detail
  **in a modal** instead of navigating away.
- The detail view returns an HTML **fragment** for htmx requests; a direct
  detail URL still renders the full page (deep links keep working).
- **All detail actions** (edit form, store/remove, tags, images, assign,
  maintenance, floor plan, …) work inside the modal.
- After a successful save the modal **closes** and the **list refreshes**.
- The detail's internal action URLs become **absolute** (`reverse`), so the
  modal works from both the per-type and the "all" lists.
- Scope: the article and storage lists, in table and card mode.

## Capabilities

### New Capabilities

- `detail-modal`: opening an entity's detail in a modal from its list, with the
  detail actions usable and the list refreshed after a save.

### Modified Capabilities

<!-- none -->

## Impact

- `article`/`storage` detail views: fragment rendering for htmx, absolute URLs.
- `hub` templates: `item.html`/`itemForm.html`, the list row/card links, the
  single modal.
- No model, migration, or dependency changes.
