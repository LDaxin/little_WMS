## Why

The detail views dump everything at once: link/copy, store actions, floor plan,
image gallery, storage contents, calendar (three forms), composition, tags,
assigned users, history, and the full edit form. On a phone the modal becomes a
long scroll, and on the desktop the edit form is always visible even when the
user only wants to look. The detail view is also identical for everyone and
every device, with no way to choose a calmer layout.

## What Changes

- **Compact header**: each detail view gets a fixed header with only identity
  (small image, name, code, type) and the primary actions (Store/Move, Edit).
  Editable values (quantity, condition, location, description, …) move out of
  the header into the field area.
- **Collapsible sections**: the remaining modules (stock, calendar,
  composition, tags, assigned, images, history) become collapsible sections with
  a count badge in the summary. Default collapsed. Scroll and context are kept.
- **Desktop layout toggle**: desktop can render the sections as an accordion
  **or** as tabs, switchable in the detail view. The choice is a URL override
  (`?layout=`); the per-user default is a new setting
  (`detail_layout_desktop`). Mobile always uses the accordion.
- **Read/Edit split**: the detail view is read-only by default, rendered as a
  label/value summary. "Edit" swaps the field area in place to the form
  (`in-place swap`); "Cancel" swaps back. Same structure, so fields are quick to
  find.
- **Saving behaviour**: a successful save returns to the read-only summary and
  refreshes the list in the background; manually closing the modal refreshes the
  list.
- **Mobile modal**: the detail modal is full-screen on mobile.
- **Scope**: all four detail views that share the templates — Article, Storage,
  Location, Tag. The header content is configured per type.

## Capabilities

### New Capabilities

- `detail-view`: the shared detail-view framework — compact header,
  collapsible sections with count summaries, the desktop accordion/tabs toggle
  (`?layout=` + `detail_layout_desktop`), the mobile accordion, and the
  read/edit split with in-place edit swap.

### Modified Capabilities

- `detail-modal`: the mobile modal is full-screen; saving keeps the detail open
  and returns to the read-only summary (list refreshed in the background);
  manually closing the modal refreshes the list.

## Impact

- `hub` app: `item.html`, `itemContent.html`, `itemForm.html`, new section
  templates (header, read-only summary), `singleModal.html` (full-screen class).
- `article`, `storage`, `location`, `tag` apps: the detail views build the new
  header/section context; `articleIncert` (and siblings) return the editable
  form for the in-place swap, including the base form.
- `organisation` app: new per-user setting `detail_layout_desktop` on the
  user profile and its Preferences form.
- `locales`: new/renamed UI strings.
