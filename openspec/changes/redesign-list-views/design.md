## Context

Every list (articles, storages, locations, tags, codes) shares one template pair:
`search.html` (search bar + table header) and `results.html` (rows). Columns are
hard-coded per type, there is no sorting, no pagination, and the results are
loaded via HTMX into `#results`. The `view_mode` setting (auto / mobile /
desktop) and the responsive sidebar already exist. `SavedView` stores only the
query today.

## Goals / Non-Goals

**Goals:**

- One data path, two renderings (table / cards), rendered server-side.
- Configurable columns and server-side sorting.
- Pagination that scales.
- A mobile layout that is not a squeezed table.
- An article list that shows the stock distribution per location.

**Non-Goals:**

- Infinite scroll.
- Multi-column sorting.
- A generic column meta-framework; keep the registry flat and small.
- Changing the location, tag and code lists in this change.

## Decisions

### Decision 1: One data path, two renderings

The search view builds one queryset/context and renders either the table partial
or the card partial. The result partial owns the whole list (header + rows, or
the card grid), so header and rows cannot drift.

### Decision 2: View mode resolution

The user's per-device list-view setting (`list_view_desktop` /
`list_view_mobile`, each `table` or `cards`) decides the rendering. The device
comes from the view-mode setting, or the client hint (`X-View-Mode`, from
`window.matchMedia`) when it is `auto`. The table/card toggle is available on
every device and overrides the setting for the current request.

### Decision 3: Column registry in code, selection in data

Each list type declares its columns in code: key, label, level (article/stock),
sortable field, and a renderer type (text, badge, location, quantity, image).
The selection (which keys, order) is data — a Saved View or the user's default.

### Decision 4: View state

URL parameters (`sort`, `cols`, `page`) are the runtime truth. A Saved View
persists them (`sort`, `columns`, `display_mode`). The user profile provides the
default when no URL parameters are present.

### Decision 5: Server-side sorting

The registry declares the sortable field per column; the view maps the `sort`
parameter to `order_by`. One column, ascending/descending toggle.

### Decision 6: Pagination

Server-side, `?page=N`. Desktop renders page numbers (replace); mobile renders a
"load more" button (append). `?page=N` is the current (desktop) or last loaded
(mobile) page.

### Decision 7: Bulk selection

Desktop keeps the checkbox column. Mobile uses a selection mode entered by a
button or a long-press on a card; a bottom action bar appears. "Select all"
means all matches (server-side over the query), not the loaded rows.

### Decision 8: The article list is a stock list

The article list is a flat table with one row per (article, location). The first
row of an article shows all article columns and the filtered total quantity
(marked when the filter hides locations, e.g. `2 (3 of 5 locations)`); the
location rows show only location and quantity. The group is collapsible.
Selection is per row. Pagination is per row; when a group crosses a page
boundary, the first row on the new page repeats the article columns.

### Decision 9: Cards

A card shows image, name, code, type, location, quantity and a condition badge.
For an article with several locations the card shows the total quantity and the
number of locations (e.g. `5 pcs · 3 locations`).

## Risks / Trade-offs

- [Group split across pages] → accepted; the repeated first row keeps the
  article identifiable.
- [Column registry complexity] → keep it flat; no meta-system.
- [Two renderings] → mitigated by one data path and one partial owning the list.

## Migration Plan

- `SavedView` gains `sort`, `columns`, `display_mode`; `UserProfile` gains a
  default column selection. Additive, no data migration.
