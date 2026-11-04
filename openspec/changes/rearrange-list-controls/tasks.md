## 1. Markup

- [x] 1.1 Wrap the search bar and the control bar in a `#listControls` container (`hub/modules/search.html`)
- [x] 1.2 Move `#scannerDiv<field>` out of the search area to directly above `#list`
- [x] 1.3 Move the advanced-search trigger into the search input-group next to the QR button; make `#queryBuilder` an anchored panel (`hub/modules/queryBuilder.html`)

## 2. Layout

- [x] 2.1 Mobile: order `#listControls` after `#list` (pinned), search bar bottom-most, control bar above it (list CSS in `header.html`)
- [x] 2.2 Advanced panel opens upward (mobile) / downward (desktop)
- [x] 2.3 Desktop and forced-desktop keep the current order; controls must not overlay the list

## 3. Verify

- [x] 3.1 Tests: search/control bar placement, advanced trigger in the search row, scanner container above `#list`
- [x] 3.2 Full suite green in Docker
- [x] 3.3 Rebuild + restart
