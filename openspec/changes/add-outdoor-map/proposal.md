## Why

§15 asks for an outdoor map: locations carry coordinates, but there is no way to
see them on a map. The `Location` model already has `latitude`, `longitude`, and
`plus_code` fields, yet nothing displays them and `plus_code` is never filled.

## What Changes

- A map page showing all locations that have coordinates on an OpenStreetMap
  (Leaflet) map, with a marker per location and a popup linking to its detail.
- The marker popup lists the storages and occasions assigned to the location.
- Plus Code (Open Location Code) support: `plus_code` is derived from the
  coordinates on save, and a Plus Code entered in the form sets the coordinates.
- A map picker on the location detail page to set coordinates by clicking.
- Location management: add/delete on the location list, reachable from the map,
  and linked storages/occasions shown on the location detail page.
- A sidebar entry point to the map.

## Capabilities

### New Capabilities

- `outdoor-map`: show locations on an OpenStreetMap map and use Open Location
  Codes (Plus Codes) for coordinates.

### Modified Capabilities

<!-- none -->

## Impact

- `location/pluscode.py` (new, pure Python), `location/models.py` (save),
  `location/forms.py`, `location/views.py`, `location/urls.py`.
- New template `location/templates/location/map.html` (Leaflet + OSM via CDN).
- `hub/templates/hub/header.html` (sidebar link).
- No new dependency.
