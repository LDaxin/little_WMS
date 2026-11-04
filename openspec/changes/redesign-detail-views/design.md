## Context

Every detail view shares two templates: `hub/modules/item.html` (full page,
extends `header.html`) and `hub/modules/itemModal.html` (fragment that includes
`itemContent.html` and auto-shows the modal). The view decides between them by
`HX-Request`. `itemContent.html` renders all modules at once and ends with
`itemForm.html`, which renders the editable form. Four views use this: Article
and Storage (rich: store actions, calendar, composition, tags, assigned,
history, images) and Location and Tag (form only, plus map/linked objects).

Relevant existing patterns to reuse:

- `list-views` resolves the per-device rendering from a `mode` URL parameter
  then the `view_mode` / `list_view_desktop` / `list_view_mobile` settings
  (`hub/columns.py: resolve_view_mode`). The client sends `X-View-Mode` from
  `window.matchMedia` (`header.html`).
- The list toggle is HTMX with the filter inputs included.
- Each module already swaps itself via HTMX (`hx-target="#tags"` etc.), e.g.
  after an add/remove.
- The "edit form" endpoints already exist: `articleIncert` / `storageIncert` /
  `locationIncert` / `tagIncert` (URL `.../<id>/i`), returning
  `itemForm.html`.
- Saving currently triggers `HX-Trigger: detail-updated`; `header.html` listens
  and hides the modal + refreshes the search input.

## Goals / Non-Goals

**Goals:**

- A compact, scannable detail view that works the same in the modal and on the
  full page, on mobile and desktop.
- Progressive disclosure: only identity + primary actions always visible; the
  rest collapsed, with a count so content is discoverable.
- A read/edit split with an in-place swap, sharing one field definition.
- Desktop can choose accordion or tabs; the default is a per-user setting.

**Non-Goals:**

- Changing the list views.
- Introducing a generic section framework or a new JS build step.
- New endpoints; reuse the existing `.../i` edit endpoints.
- Reworking the individual module internals (tags, images, calendar, …) beyond
  placing them into sections.

## Decisions

### Decision 1: One detail view for modal and full page

`itemContent.html` stays the single source. `item.html` and `itemModal.html`
only wrap it. Every improvement applies to both; no second layout to maintain.

### Decision 2: Header = identity + actions, field area = values

The header holds only identity (small image, name, code, type) and the primary
actions (Store/Move, Edit). The editable values (quantity, condition, location,
description, custom fields) move into the field area. This avoids showing a
value twice and avoids a stale header while editing.

### Decision 3: Native `<details>` for the accordion, tabs as a desktop variant

The accordion uses native `<details>/<summary>`: no JS, survives HTMX swaps,
works identically in modal and page. Each summary carries a count badge rendered
server-side. Tabs are a desktop-only alternative over the same sections. The
section list is a server-side collection (name, label, count, template) so
accordion and tabs can never drift.

### Decision 4: Layout resolution mirrors `list-views`

Add `detail_layout_desktop` to the user profile (`accordion` default, `tabs`
optional) and a `layout` URL parameter override, resolved exactly like
`resolve_view_mode`. Mobile ignores the setting and always uses the accordion;
the toggle is desktop-only. Reusing the pattern keeps the mental model the same
as the list.

### Decision 5: Read/edit split with in-place swap

The field area renders a read-only label/value summary by default (from the
same field definitions as the form, so labels and order match). Edit swaps the
field area to the form via the existing `.../i` endpoint (HTMX `hx-get` into the
field-area container); Cancel swaps back to the summary. The `.../i` endpoints
are extended to return the full field set (base + article form), which they
currently truncate.

### Decision 6: Save keeps the detail open, manual close refreshes the list

On save the field area returns to the read-only summary with fresh values and
the list is refreshed in the background (`detail-updated` reused). Closing the
modal manually also refreshes the list. This also removes the stale hidden
`version` on the full page: entering edit re-fetches the form (and its current
`version`), so a second save is not falsely rejected.

### Decision 7: Full-screen modal on mobile

The modal container gets Bootstrap's `modal-fullscreen-sm-down` so mobile gets
the full screen and desktop stays a window. One class, no extra JS.

## Risks / Trade-offs

- **Summary and form can drift** → derive both from the same field list; the
  summary renders the bound values, the form renders the fields.
- **HTMX swap targets inside the modal** → keep one stable container id for the
  field area; the swap replaces only that container.
- **Tabs add a second rendering path on desktop** → both paths read the same
  section collection; tabs are a pure presentation switch.
- **Existing tests assert the old templates/flow** (e.g. `test_detail_modal`) →
  update them in the same change; keep them as the regression net for the
  one-view/modal behaviour.
- **Full-screen modal changes the close affordance on mobile** (only the X, no
  swipe) → acceptable; the X stays reachable and the list stays behind.

## Migration Plan

No data migration. Only a profile field (`detail_layout_desktop`) with a
default. Rollback is reverting the templates/views; the setting can stay.

## Open Questions

Resolved during implementation, per the agreed approach:

- Exact section order (e.g. stock → calendar → tags → assigned → images →
  composition → history).
- Which fields belong in the header per type (Article/Storage vs Location/Tag).
- Whether Store actions are a section or stay near the header.
- The count shown per section when "empty".
