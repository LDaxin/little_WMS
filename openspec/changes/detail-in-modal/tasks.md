## 1. Detail fragment

- [x] 1.1 Extract the body of `hub/modules/item.html` into a shared `itemContent.html`
- [x] 1.2 Render the fragment for htmx requests in the `article` and `storage` detail views; full page otherwise
- [x] 1.3 The fragment shows `#modalsingle` after it is swapped in

## 2. Absolute action URLs

- [x] 2.1 Build the detail action URLs (update, store, remove, store-search, tags, assign, images, floor-plan, scanner) with absolute paths in the `article` and `storage` detail views

## 3. Triggers in the list

- [x] 3.1 Table edit buttons and card links: `hx-get` the detail URL into `#modalBodysingle`
- [x] 3.2 Keep the `href` fallback; disable the card stretched-link while the modal is open

## 4. Save behaviour

- [x] 4.1 The update views send `HX-Trigger: detail-updated`
- [x] 4.2 JS: on `detail-updated` close `#modalsingle` and refresh the list

## 5. Verify

- [x] 5.1 Tests: fragment endpoint returns no `<html>`, list links carry `hx-get`, direct URL renders the full page
- [x] 5.2 Full suite green in Docker
- [x] 5.3 Rebuild + restart
- [ ] 5.4 Manual: open from table and card, use every detail action inside the modal

## 6. Native actions on htmx

- [x] 6.1 Images (upload, primary, delete) return the gallery fragment for htmx
- [x] 6.2 Maintenance, lend and borrow return the calendar fragment for htmx
