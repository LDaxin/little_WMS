# floor-plans Specification

## Purpose
TBD - created by archiving change add-floor-plans. Update Purpose after archive.
## Requirements
### Requirement: Floor plan per storage

The system SHALL let a storage have one floor plan with an uploaded image, and
SHALL let a user upload or replace that image.

#### Scenario: Upload a plan

- **WHEN** a user uploads an image as the floor plan of a storage
- **THEN** the plan is stored and shown for that storage

#### Scenario: Replace a plan

- **WHEN** a user uploads a new image for a storage that already has a plan
- **THEN** the image is replaced and the existing areas are kept

### Requirement: Draw plan areas

The system SHALL let a user draw rectangular areas on a floor plan and link each
area to a storage. Area positions SHALL be stored relative to the plan image so
they scale with it.

#### Scenario: Draw an area

- **WHEN** a user draws a rectangle on the plan and links it to a storage
- **THEN** the area is stored with its position and the linked storage

#### Scenario: Areas survive a plan change

- **WHEN** the plan image is replaced
- **THEN** the drawn areas remain

### Requirement: Navigate the plan

The system SHALL show the floor plan with its areas and SHALL open the linked
storage when an area is clicked, preferring that storage's own floor plan when
it has one. The plan SHALL offer a link back to its storage's detail page.

#### Scenario: Click an area whose storage has a plan

- **WHEN** a user clicks an area linked to a storage that has a floor plan
- **THEN** that storage's floor plan is opened

#### Scenario: Click an area whose storage has no plan

- **WHEN** a user clicks an area linked to a storage without a floor plan
- **THEN** that storage's detail page is opened

#### Scenario: Return to the storage

- **WHEN** a user opens a floor plan
- **THEN** the plan links back to its storage's detail page

### Requirement: Highlight an area

The system SHALL highlight the area of a given storage when the plan is opened
with that storage selected.

#### Scenario: Highlight

- **WHEN** the plan is opened with a storage selected
- **THEN** the area linked to that storage is highlighted

