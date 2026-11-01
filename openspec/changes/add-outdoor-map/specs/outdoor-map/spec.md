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

### Requirement: Map marker links

The system SHALL list the storages and occasions assigned to a location in that
location's map popup, each as a link to the object's detail page.

#### Scenario: Linked storages are listed

- **WHEN** a location has storages assigned to it
- **THEN** the marker popup lists those storages as links

#### Scenario: Linked occasions are listed

- **WHEN** a location has occasions assigned to it
- **THEN** the marker popup lists those occasions as links

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

### Requirement: Set coordinates on a map

The system SHALL let a user set a location's coordinates by clicking or dragging
a marker on a map on the location's detail page.

#### Scenario: Click sets coordinates

- **WHEN** a user clicks a point on the location's map
- **THEN** the location's latitude and longitude fields are set to that point

#### Scenario: Existing coordinates are shown

- **WHEN** a location already has coordinates
- **THEN** the map shows a marker at those coordinates

### Requirement: Manage locations

The system SHALL let a user add and delete locations from the location list, and
SHALL provide a link to the location list from the map.

#### Scenario: Add a location

- **WHEN** a user opens the location list
- **THEN** an add action is available

#### Scenario: Reach the location list from the map

- **WHEN** a user opens the map
- **THEN** a link to the location list is available

### Requirement: Location detail shows linked objects

The system SHALL show the storages and occasions assigned to a location on the
location's detail page, each as a link.

#### Scenario: Linked objects on the detail page

- **WHEN** a user opens a location that has storages or occasions assigned
- **THEN** those objects are listed as links
