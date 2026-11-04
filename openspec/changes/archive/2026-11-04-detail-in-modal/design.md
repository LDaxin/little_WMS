## Context

The list pages already include an empty single-item modal (`#modalsingle` via
`items.html`), the detail views set `modalId: "single"`, and `itemForm.html`
uses `#modalsingle` as its Select2 parent — the modal was intended but never
wired. Today the detail view renders the full page (`item.html`, which extends
`header.html`), and the list row/card links navigate there.

## Goals / Non-Goals

**Goals:**

- Open the detail in a modal from the list (table edit button and cards), for
  articles and storages.
- Keep the full detail page for direct URLs (deep links).
- Make every detail action usable inside the modal.
- On save: close the modal and refresh the list.

**Non-Goals:**

- Changing the detail content itself.
- The location and code lists (they still use the old table).
- Deleting/navigation semantics beyond the modal.

## Decisions

### Decision 1: One content partial, two renderings

Extract the body of `hub/modules/item.html` into a shared partial
(`itemContent.html`). `item.html` keeps extending `header.html` and includes it
(the direct/deep-link page). For htmx requests the detail view renders the
partial (plus a small "show the modal" script), keyed on the `HX-Request`
header. No content is duplicated.

### Decision 2: Absolute action URLs in the detail context

The detail's internal URLs are relative today (`./<id>/update`, `storeUrl`,
`tagAddUrl`, `imageBaseUrl`, the scanner, …). Loaded into a modal on `/article/`
or `/storage/` they would resolve against the list URL and break. Build them
with `reverse(...)` so the modal works from the per-type and the "all" lists
alike. `_store_actions_context`'s `storeUrl + "-search"` keeps working with an
absolute `storeUrl`.

### Decision 3: Trigger and show

The list edit button and the card link get `hx-get="<detail-url>"`,
`hx-target="#modalBodysingle"`, `hx-swap="innerHTML"`; the returned fragment
shows `#modalsingle`. The `href` stays as a no-JS/deep-link fallback. The
`.stretched-link` on cards is disabled while the modal is open (as selection
already does).

### Decision 4: Save closes and refreshes

The update views add an `HX-Trigger: detail-updated` response header. A page
listener closes `#modalsingle` and dispatches `refresh` on the search input
(which already has `hx-trigger="load, keyup …, refresh"`), reloading the list.

## Risks / Trade-offs

- [Select2 / scanner / map inside the modal] → they already target `#modalsingle`
  and element ids; verify each in the modal.
- [Relative-URL pitfall on the "all" list] → mitigated by Decision 2.
- [Re-running the detail script on every open] → keep the show-script minimal and
  idempotent.
- [Nested htmx targets] → the modal body is a distinct target; no conflict with
  the list.

## Migration Plan

Template/view only — no data or schema changes. Deploy by rebuilding the image;
rollback by reverting the commit.
