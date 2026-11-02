## ADDED Requirements

### Requirement: The scanned article's image is shown

The system SHALL show the scanned article's primary image on the movement page
for visual confirmation, and SHALL let the user turn this off.

#### Scenario: Article with an image

- **WHEN** the user scans an article that has an image and the setting is on
- **THEN** the active card shows the article's primary image

#### Scenario: Article without an image

- **WHEN** the user scans an article that has no image
- **THEN** no image is shown

#### Scenario: Image turned off

- **WHEN** the user has turned the image off
- **THEN** no image is shown
