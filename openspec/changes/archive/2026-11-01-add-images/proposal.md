## Why

Articles and storages are identified by name and code only. A photo makes them
recognisable at a glance — in lists, on the detail page, and while scanning
during movement. §15 of the Lastenheft asks for images; this change delivers the
image part (floor plans and the outdoor map follow later).

## What Changes

- New `ArticleImage` and `StorageImage` models: multiple images per object, one
  primary, with caption and order.
- Upload (including from a phone camera), delete, and set-primary actions on the
  article and storage detail pages.
- Automatic resize on upload plus a generated thumbnail.
- Thumbnail in the article/storage list, gallery on the detail page.
- Media storage: `MEDIA_ROOT`/`MEDIA_URL` settings and dev serving; Pillow
  dependency.

## Capabilities

### New Capabilities

- `images`: article and storage images — upload, primary image, ordering,
  resize/thumbnail, list thumbnail and detail gallery.

### Modified Capabilities

<!-- none -->

## Impact

- New models + migration in `article` and `storage`; new views/urls/templates.
- `src/little_wms/settings.py` (media), `src/little_wms/urls.py` (dev media),
  `requirements.txt` (Pillow).
- `hub/templates/hub/modules/results.html` (list thumbnail),
  `hub/templates/hub/modules/item.html` (gallery).
- **Deferred**: floor plans, outdoor map, movement-scan visual confirmation.
