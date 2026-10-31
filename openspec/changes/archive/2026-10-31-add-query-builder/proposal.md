## Why

§9 describes a visual query builder for power users: build filters graphically
(field/operator/value, AND/OR, nested groups, NOT) instead of typing a search.
Today the article list only has a single quick-search field.

## What Changes

- A `querybuilder` app with a `QueryParser` translating the client JSON query
  (AND/OR/NOT, nested groups) into Django `Q` objects, with a whitelist of
  allowed fields and operators per field type.
- An "Advanced" query builder on the article list (vanilla JS); the search view
  applies the parsed query.

## Capabilities

### New Capabilities

- `query-builder`: a visual query builder and its JSON→Q parser.

### Modified Capabilities

<!-- none -->

## Impact

- New `querybuilder` app; the article search view accepts a `query` parameter.
- **Deferred**: presets (save/share); drag & drop; the other use sites (storage
  list, QR print, export, packlist, movement search, dashboard widgets).
