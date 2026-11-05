## 1. Structure: header, sections, read-only summary

- [x] 1.1 Define the section list per detail view in the view context (key, label, count, template), reusing the existing module templates
- [x] 1.2 Add a compact header partial: small image, name, code, type, plus Store/Move and Edit; per-type header fields
- [x] 1.3 Add a read-only summary partial that renders the form's fields as label/value from the same field list
- [x] 1.4 Rework `itemContent.html` to header + collapsible sections + field area; keep `item.html` / `itemModal.html` wrappers unchanged
- [x] 1.5 Render the accordion with native `<details>/<summary>` and a count badge per summary
- [x] 1.6 Wire Article and Storage detail views to the new context

## 2. Read/Edit split

- [x] 2.1 Add a stable field-area container id plus Edit and Cancel actions in the header/field area
- [x] 2.2 Extend the `.../i` endpoints (`articleIncert`, `storageIncert`, `locationIncert`, `tagIncert`) to return the full field set (base + object form)
- [x] 2.3 Swap the field area to the form on Edit (HTMX) and back to the read-only summary on Cancel
- [x] 2.4 On save: return to the read-only summary with fresh values, keep the detail open, refresh the list in the background
- [x] 2.5 On manual modal close: refresh the list
- [x] 2.6 Remove the stale hidden `version` path on the full page (form re-fetched on Edit carries the current version)

## 3. Desktop layout toggle and setting

- [x] 3.1 Add `detail_layout_desktop` (`accordion` default, `tabs`) to the user profile, with migration
- [x] 3.2 Add layout resolution: `layout` URL parameter wins, else `detail_layout_desktop`; mobile forces accordion
- [x] 3.3 Render the tabs layout over the same section list
- [x] 3.4 Add the desktop-only accordion/tabs toggle and carry `layout` through the detail HTMX requests
- [x] 3.5 Add the setting to the Preferences form and page

## 4. Mobile and remaining detail views

- [x] 4.1 Add `modal-fullscreen-sm-down` to the detail modal container
- [x] 4.2 Apply the header and section configuration to the Location and Tag detail views
- [x] 4.3 Add/update translation strings (English source, German catalogue)

## 5. Tests and verification

- [x] 5.1 Update `article/tests/test_detail_modal.py` for the new save/close behaviour
- [x] 5.2 Add tests: compact header, collapsed sections with counts, read-only summary, Edit/Cancel swap, layout resolution (param wins, setting default, mobile accordion)
- [x] 5.3 Run the full test suite in Docker; must be green
- [x] 5.4 Rebuild Docker (`docker compose build && up -d`) and report how to test (URL, credentials)

## 6. Header rework (mobile first)

- [x] 6.1 Rebuild `itemHeader.html`: name row on top, image (~110 px, rounded) left with type / condition / tags / quantity·locations stacked right, code and action row below
- [x] 6.2 Extend the article `detailHeader` context with condition, total quantity, unit, storage-location count and tags
- [x] 6.3 Keep the existing actions (copy link, floor plan, store, edit) and add an "Open" action (full detail page); hide article-only fields for Storage/Location/Tag
