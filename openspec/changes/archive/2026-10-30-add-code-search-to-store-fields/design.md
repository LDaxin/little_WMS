## Context

`storeActions.html` and `storageContents.html` already include the QR scanner
(`hub/modules/qrScanner.html`) but their inputs only accept a code. The
`little-wms-code-input` standard requires code OR name search as well.

## Goals / Non-Goals

**Goals:**

- Both store fields find the object by code or name, with live suggestions.
- Keep the existing scanner.

**Non-Goals:**

- Changing the store logic itself.
- Other code fields (already compliant).

## Decisions

### Decision 1: Store-target search (article app)

New view `storeTargetSearch(request, typ, articleId)` returning
`hub/modules/storeTargetResults.html`: storages and container articles matching
name or code. Each suggestion posts its code to the existing store URL
(`./<id>/store`) targeting `#storeActions`.

### Decision 2: Store-article search (storage app)

New view `storeArticleSearch(request, typ, storageId)` returning
`hub/modules/storeArticleResults.html`: articles matching name or code. Each
suggestion posts its code to the existing store URL targeting
`#storageContents`.

### Decision 3: Field markup

Follow the standard: `hx-get` on the input, a `#…Results` container, the
`qrScanner.html` include and its `scannerDiv`.

## Risks / Trade-offs

- [Two more endpoints] → small, guarded by the same permissions as the store
  views (`article.move_all` / `article.move_all`).

## Migration Plan

- No model or migration changes.

## Open Questions

<!-- none -->
