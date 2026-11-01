## 1. Plus Code

- [x] 1.1 `location/pluscode.py` with `encode(lat, lng)` and `decode(code)`
- [x] 1.2 Round-trip test against reference values

## 2. Model & Form

- [x] 2.1 `Location.save()` derives `plus_code` from coordinates
- [x] 2.2 `FormLocation` decodes an entered Plus Code into coordinates
- [x] 2.3 Tests for both

## 3. Map

- [x] 3.1 Map view (`/location/map`) with Leaflet + OSM
- [x] 3.2 Template `location/templates/location/map.html`
- [x] 3.3 URL
- [x] 3.4 Sidebar link
- [x] 3.5 View test (200, markers for locations with coordinates)

## 4. Map links

- [x] 4.1 Map view prefetches linked storages and occasions
- [x] 4.2 Marker popup lists linked storages and occasions as links
- [x] 4.3 Test for the popup links

## 5. Coordinate picker

- [x] 5.1 Map picker on the location detail page (click/drag sets lat/long)
- [x] 5.2 Test that the picker is rendered

## 6. Location management

- [x] 6.1 Add/delete actions on the location list
- [x] 6.2 Link to the location list from the map
- [x] 6.3 Location detail page lists linked storages and occasions
- [x] 6.4 Tests

## 7. Verify

- [x] 7.1 Full test suite green in Docker
- [x] 7.2 Rebuild Docker and restart the container
- [x] 7.3 Update Lastenheft status (§15 Outdoor Map)
