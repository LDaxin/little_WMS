## ADDED Requirements

### Requirement: Article and storage images

The system SHALL let an article and a storage each have multiple images. Each
image SHALL have an optional caption and an order, and at most one image per
object SHALL be the primary image.

#### Scenario: Multiple images

- **WHEN** a user adds several images to an article
- **THEN** all images are stored and shown in their order

#### Scenario: One primary image

- **WHEN** a user marks an image as primary
- **THEN** that image is the primary one and any previous primary is cleared

### Requirement: Upload images

The system SHALL let a user upload an image to an article or storage, including
directly from a phone camera.

#### Scenario: Upload from the detail page

- **WHEN** a user selects or captures an image on the detail page
- **THEN** the image is stored and appears in the gallery

#### Scenario: First image becomes primary

- **WHEN** a user uploads the first image of an object
- **THEN** that image is the primary image

### Requirement: Delete an image

The system SHALL let a user delete an image from an article or storage.

#### Scenario: Delete

- **WHEN** a user deletes an image
- **THEN** the image is removed from the gallery

### Requirement: Resize and thumbnail

The system SHALL resize an uploaded image to a bounded size and SHALL generate a
thumbnail for it.

#### Scenario: Large upload

- **WHEN** a user uploads an image larger than the maximum size
- **THEN** the stored image is scaled down and a thumbnail is generated

### Requirement: Image display

The system SHALL show a thumbnail in the article and storage list and a gallery
on the detail page.

#### Scenario: List thumbnail

- **WHEN** an object has a primary image
- **THEN** its thumbnail is shown in the list

#### Scenario: Detail gallery

- **WHEN** a user opens the detail page of an object with images
- **THEN** the images are shown as a gallery
