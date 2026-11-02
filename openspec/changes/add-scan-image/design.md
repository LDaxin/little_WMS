## Context

`Article.primary_image` returns the article's primary image (or the first one),
and `BaseImage.thumbnail` is a generated thumbnail. The movement page's active
card already shows the last scanned article; the search results already render a
thumbnail this way. Per-user UI settings live on `UserProfile` and are exposed to
templates through the `active_organisation` context processor.

## Goals / Non-Goals

**Goals:**

- Show the scanned article's primary image on the movement page for visual
  confirmation.
- Per-user on/off switch.

**Non-Goals:**

- Images in the buffer list (only the active card, as specified in §15).
- Images for storages or containers on scan.
- A new image model or dependency.

## Decisions

### Decision 1: Reuse `primary_image` and the thumbnail

The active card renders `active.primary_image.thumbnail` when the setting is on
and an image exists — the same pattern as `hub/modules/results.html`.

### Decision 2: Setting on `UserProfile`

`image_on_scan` (default on) follows the existing per-user settings pattern and
sits next to the sound/vibration settings in the scan-feedback section.

## Risks / Trade-offs

- [Extra query] → the active article is already loaded; `primary_image` reads its
  images, a small extra query per buffer render. Acceptable.

## Migration Plan

- Add one column to `organisation_userprofile` with a default. Rollback: drop it.
