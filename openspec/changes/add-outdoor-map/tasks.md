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

## 4. Verify

- [x] 4.1 Full test suite green in Docker
- [x] 4.2 Rebuild Docker and restart the container
- [x] 4.3 Update Lastenheft status (§15 Outdoor Map)
