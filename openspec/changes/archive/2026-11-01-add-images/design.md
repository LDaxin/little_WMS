## Context

Articles and storages have no images today. The project has no media
configuration (`MEDIA_ROOT`/`MEDIA_URL`) and no Pillow dependency. The article
and storage detail pages are rendered from `hub/templates/hub/modules/`
(`item.html` + `itemForm.html`), the lists from `results.html`.

## Goals / Non-Goals

**Goals:**

- Multiple images per article and storage, one primary, with caption and order.
- Upload (phone camera), delete, set-primary.
- Resize on upload + generated thumbnail.
- Thumbnail in the list, gallery on the detail page.

**Non-Goals:**

- Floor plans and the outdoor map (§15 later phases).
- Movement-scan visual confirmation (deferred).
- Image editing/cropping.

## Decisions

### Decision 1: Two models on a shared abstract base

`ArticleImage` and `StorageImage` share an abstract `BaseImage` (`image`,
`thumbnail`, `is_primary`, `caption`, `order`). Two concrete models keep the
foreign keys simple; a generic relation would be over-engineering for two
owners.

### Decision 2: Resize and thumbnail on save with Pillow

`ImageField` already requires Pillow, so no extra dependency is added. On save
the image is scaled to a maximum edge (1600px) and a thumbnail (300px) is
written to a second field. This avoids a thumbnail service or a new dependency
(`easy-thumbnails`/`imagekit`).

### Decision 3: Media storage

`MEDIA_ROOT` under `data/media`, `MEDIA_URL` `/media/`, served by Django in dev
via `static()` in the root urlconf. Images live on the filesystem, not in the
DB (§37).

### Decision 4: Plain form upload, no JS library

Upload is a normal multipart form (with `accept="image/*" capture="environment"`
for the camera) posted to a small view; the gallery is re-rendered. No upload
widget library.

## Risks / Trade-offs

- [Large phone photos] → resized on upload; thumbnail for lists.
- [Orphaned files on delete] → delete the file in the model's `delete()`.
- [Media not served in production] → out of scope; dev serving only for now.

## Migration Plan

- New tables `article_articleimage`, `storage_storageimage`; no data migration.
- Rollback: drop the tables.
