## Context

`Location` already has `latitude`, `longitude`, and `plus_code` fields, and the
location form already exposes them. The app loads front-end libraries from CDNs
(select2, htmx, html5-qrcode) and has no map. The locations list page
(`/location/`) is currently not linked from the sidebar.

## Goals / Non-Goals

**Goals:**

- Show locations with coordinates on an OpenStreetMap map.
- Derive a Plus Code from coordinates and vice versa.

**Non-Goals:**

- Marker clustering, routing, offline maps, geocoding/search.
- Editing coordinates directly on the map.

## Decisions

### Decision 1: Leaflet + OSM tiles via CDN

Leaflet is loaded from a CDN like the other front-end libraries; tiles come from
OpenStreetMap. No new Python dependency, no API key.

### Decision 2: Plus Code in pure Python

`location/pluscode.py` implements the Open Location Code encode/decode
algorithm (~50 lines) instead of adding the `openlocationcode` package. The
algorithm is small and well-specified; a round-trip test pins it.

### Decision 3: Derive on save, decode in the form

`Location.save()` fills `plus_code` from the coordinates when coordinates are
set and the code is empty. `FormLocation.clean()` decodes an entered Plus Code
into coordinates when coordinates are empty. This keeps the fields consistent
without a separate action.

### Decision 4: Dedicated map page

The map lives on its own page (`/location/map`) with a sidebar entry, since a
full-width map does not fit the list/detail layout.

## Risks / Trade-offs

- [Plus Code correctness] → a round-trip test (encode → decode) pins the
  implementation against known reference values.
- [Locations without coordinates] → simply omitted from the map.

## Migration Plan

- No schema change; the fields already exist.
- Rollback: remove the view/url/template and the sidebar link.
