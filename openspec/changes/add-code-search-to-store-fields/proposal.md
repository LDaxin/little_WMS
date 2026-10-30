## Why

Two store fields still only accept a code with a scanner but no search:
`storeActions.html` (the store-target field on an article) and
`storageContents.html` (the store-article field on a storage). Per the
`little-wms-code-input` standard, a code field must find the object by code OR
name and offer the scanner.

## What Changes

- The **store-target** field (article detail) finds storages/containers by code
  **or name**, with live suggestions, plus the QR scanner.
- The **store-article** field (storage detail) finds articles by code **or
  name**, with live suggestions, plus the QR scanner.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `movement`: the store-target field finds by code or name (with scanner).
- `storage-management`: the store-article field finds by code or name.

## Impact

- `hub/modules/storeActions.html`, `hub/modules/storageContents.html`.
- Search views + suggestion partials + URLs in the `article` and `storage` apps.
- No model or migration changes.
