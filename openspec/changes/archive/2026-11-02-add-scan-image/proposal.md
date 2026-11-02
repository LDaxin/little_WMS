## Why

§15 lists movement visualization as part of the images feature: when an article
is scanned, its image appears for visual confirmation, configurable on/off. The
image feature is otherwise built (upload, primary image, thumbnail, list and
detail display), but this part was never finished.

## What Changes

- Per-user setting `image_on_scan` on `UserProfile` (default on).
- A "Show image" checkbox in the preferences page's scan-feedback section.
- The movement page's active card shows the scanned article's primary image
  (thumbnail) when the setting is on and the article has an image.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `movement`: the active card shows the scanned article's primary image,
  configurable per user.

## Impact

- `organisation` app: `UserProfile` field + migration.
- `hub` app: preferences view and template.
- `movement` app: buffer template.
