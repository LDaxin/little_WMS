## Why

Storages are hierarchical, but there is no way to see where a storage sits on a
plan. §15 asks for floor plans: upload a plan for a storage level and mark the
sub-storages as clickable areas, so a user can navigate the warehouse visually.

## What Changes

- New `FloorPlan` (one per storage, with an uploaded image) and `FloorPlanArea`
  (a rectangle on the plan, optionally linked to a storage) models.
- Upload/replace the plan image for a storage (Stage 1).
- A drawing editor: draw rectangles on the plan and link each to a storage
  (Stage 2), stored as relative coordinates.
- A plan view with clickable areas; clicking an area opens its storage.
- Highlight an area via a URL parameter (for "Where is X?" / QR scan).

## Capabilities

### New Capabilities

- `floor-plans`: upload a plan for a storage, draw storage areas on it, and
  navigate the plan by clicking areas.

### Modified Capabilities

<!-- none -->

## Impact

- New models + migration in `storage`; new views/urls/templates.
- `hub/templates/hub/modules/item.html` (link to the plan),
  new `hub/modules/floorPlan*.html`.
- Reuses the media setup from `add-images`.
- **Deferred**: outdoor map, movement-scan visual confirmation.
