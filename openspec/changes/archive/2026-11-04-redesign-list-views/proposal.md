## Why

The list views are one shared table with hard-coded columns, no sorting, no
pagination, and no mobile layout. For a warehouse the lists should be dense and
configurable on desktop and card-based on mobile. The article list should show
where each article actually sits (one row per storage location), not just one
row per article.

## What Changes

- **Two renderings, one data path**: a table (desktop) and cards (mobile), both
  rendered server-side from the same query. The client sends a view-mode hint;
  the user's `view_mode` setting wins. Desktop gets a table/card toggle.
- **Column registry**: the available columns per list type are defined in code;
  the selection (which columns, order) is data.
- **View state**: URL parameters are the runtime truth, a Saved View persists
  them, the user profile provides the default.
- **Server-side sorting** driven by the registry.
- **Pagination**: page numbers on desktop, "load more" on mobile.
- **Bulk selection**: checkbox column on desktop, a selection mode (button and
  long-press) on mobile; "select all" means all matches.
- **Article list as a stock list**: one row per (article, location), grouped
  visually, first row shows the article columns and the filtered total, the
  location rows show location and quantity; collapsible; selection per row.
- **Storage list**: the same table/card framework with its own columns.

## Capabilities

### New Capabilities

- `list-views`: the shared table/card framework — rendering, columns, view
  state, sorting, pagination, bulk selection.

### Modified Capabilities

- `article-management`: the article list becomes a grouped stock list with
  configurable columns and cards.
- `storage-management`: the storage list uses the shared framework with its own
  columns and cards.

## Impact

- `hub` app: the shared list templates and the column registry.
- `article` app: the article list/search views and the stock grouping.
- `storage` app: the storage list/search views.
- `savedviews` app: `sort`, `columns`, `display_mode` on `SavedView`.
- `organisation` app: a per-user default column selection.
