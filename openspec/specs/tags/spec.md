# Tags Specification

## Purpose

Organise articles and storages with tags: categories, hierarchical tags with
colour and icon, and tag chips on the detail pages.

## Requirements

### Requirement: Tags and categories

The system SHALL let the user create tags with a name, an optional parent, an
optional category, a colour, and an icon.

#### Scenario: Create a tag

- **WHEN** the user adds a tag
- **THEN** the tag is created with its colour and icon

#### Scenario: Hierarchical tags

- **WHEN** a tag has a parent
- **THEN** its display name is the parent path plus its own name

### Requirement: Tag chips on objects

The system SHALL show an object's tags as chips and SHALL let the user add and
remove tags on an article or storage.

#### Scenario: Add a tag to an article

- **WHEN** the user adds a tag to an article
- **THEN** the tag appears as a chip on the article

#### Scenario: Remove a tag

- **WHEN** the user removes a tag from an article
- **THEN** the tag no longer appears on the article

### Requirement: Delete tags

The system SHALL soft-delete a tag.

#### Scenario: Delete a tag

- **WHEN** the user deletes a tag
- **THEN** the tag is soft-deleted
