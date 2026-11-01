## Context

The `add-images` change added media storage (`MEDIA_ROOT`, dev serving) and
Pillow. Storages are hierarchical (`Storage.parent`). The storage detail page is
`hub/templates/hub/modules/item.html`.

## Goals / Non-Goals

**Goals:**

- One floor plan per storage with an uploaded image.
- Draw rectangular areas, each linked to a storage.
- Clickable areas that navigate; highlight a selected area.

**Non-Goals:**

- Outdoor map / Plus Codes.
- Polygons (rectangles only for now).
- Movement-scan visual confirmation.

## Decisions

### Decision 1: Two models in the `storage` app

`FloorPlan` (`storage` OneToOne, `name`, `image`) and `FloorPlanArea`
(`floor_plan` FK, `storage` FK nullable, `shape` JSON, `label`, `color`). The
`FloorPlan.drawing` JSON field from the Lastenheft is dropped — the areas are
relational and queryable, so a second JSON copy would be redundant.

### Decision 2: Relative coordinates

An area's `shape` is `{"x": 0.1, "y": 0.2, "w": 0.3, "h": 0.15}` with values in
0–1 relative to the image. The plan then scales with the viewport without
recomputing positions.

### Decision 3: SVG overlay, vanilla JS editor

The plan is an `<img>` with an absolutely positioned `<svg viewBox="0 0 1 1"
preserveAspectRatio="none">` overlay. The editor draws rectangles with plain
mouse events (no drawing library) and posts the areas as JSON.

### Decision 4: Dedicated plan page

The plan lives on its own page (`/storage/<typ>/<id>/plan`) with an editor mode,
linked from the storage detail page. A large plan does not fit the detail form.

## Risks / Trade-offs

- [Image aspect ratio] → the SVG overlay matches the image box, so relative
  coordinates map correctly.
- [Areas after image replace] → areas are kept; the user re-aligns if needed.
- [No polygons] → rectangles cover rooms and shelves; polygons can be added later.

## Migration Plan

- New tables `storage_floorplan`, `storage_floorplanarea`; no data migration.
- Rollback: drop the tables.
