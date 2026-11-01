## ADDED Requirements

### Requirement: Location map

The system SHALL show all locations that have coordinates on an OpenStreetMap
map, with one marker per location. Each marker SHALL show the location's name
and SHALL link to the location's detail page.

#### Scenario: Locations with coordinates are shown

- **WHEN** a user opens the map
- **THEN** every location with latitude and longitude is shown as a marker

#### Scenario: Locations without coordinates are omitted

- **WHEN** a location has no coordinates
- **THEN** it is not shown on the map

#### Scenario: Open a location from the map

- **WHEN** a user clicks a marker
- **THEN** the popup shows the location's name and a link to its detail page

### Requirement: Plus Code

The system SHALL derive a location's Plus Code (Open Location Code) from its
coordinates when it is saved, and SHALL set the coordinates from a Plus Code
entered in the location form.

#### Scenario: Plus Code derived on save

- **WHEN** a location with coordinates and no Plus Code is saved
- **THEN** its Plus Code is filled from the coordinates

#### Scenario: Coordinates from a Plus Code

- **WHEN** a user enters a Plus Code in the location form without coordinates
- **THEN** the coordinates are set from the Plus Code
