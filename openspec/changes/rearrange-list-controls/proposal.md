## Why

On a phone the list controls (search field, columns, table/cards toggle,
select) sit above the list — out of reach for the thumb. The advanced-search
trigger lives in its own row below the controls, and the QR scanner panel is
bolted to the search bar, so its position follows the search bar.

## What Changes

- **Mobile control placement**: on the list pages the search bar and the
  control bar move **below** the list and stay **pinned** at the bottom — the
  search bar is the bottom-most element, the control bar sits directly above
  it. Applies to both table and card mode and to the per-type and "all" lists.
- **Advanced trigger with the search field**: the advanced-search trigger moves
  into the search field row, next to the QR button, on mobile **and** desktop
  (article list today; storage later, out of scope here).
- **Advanced panel direction**: the advanced panel opens **upward on mobile**
  and **downward on desktop**.
- **Scanner panel above the list**: the QR scanner panel always opens **above**
  the list, independent of where the search bar sits.

Out of scope (noted for later): the floating action buttons (add / delete /
export / QR); the advanced search on the storage list.

## Capabilities

### New Capabilities

- `list-view-controls`: placement and thumb-reachability of the list-page
  controls (search bar, control bar, advanced trigger, advanced panel, scanner
  panel) on desktop and mobile.

### Modified Capabilities

<!-- none: list-views is still an unarchived change; no existing spec changes. -->

## Impact

- `hub` templates: `modules/search.html`, `modules/queryBuilder.html`,
  `modules/list.html`, `header.html` (list CSS).
- No view, model, migration, or dependency changes.
