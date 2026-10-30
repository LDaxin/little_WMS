# Stock and Composition Specification

## Purpose

Separate an article's identity from its quantity: quantity lives on `Stock`
lines per location, and a storage location can declare a composition (what it
should contain) with per-location and global minimums.

## Requirements

### Requirement: Quantity lives on stock lines

The system SHALL store an article's quantity as `Stock` lines, one per location,
with a "not stored" line (`stored` is empty) for the unplaced quantity.

#### Scenario: New article starts not stored

- **WHEN** an article is created
- **THEN** it has a single "not stored" stock line

#### Scenario: One line per location

- **WHEN** an article is stored in a location that already has a line
- **THEN** the quantity is added to that line instead of creating a second one

### Requirement: Composition declares a target

The system SHALL let a storage location declare a composition of article bases
with an optional target quantity (`soll_menge`) and an optional minimum
(`mindestmenge`).

#### Scenario: Composition status

- **WHEN** a location has a composition
- **THEN** the system shows, per item, the actual quantity, the target, the minimum, and whether it is underfilled or needs a refill

#### Scenario: Over-allocation

- **WHEN** the sum of targets across all locations exceeds the number of articles of that base
- **THEN** the system flags the base as over-allocated

### Requirement: Minimums and refill hints

The system SHALL support a per-location minimum and a global minimum per base,
and SHALL show a refill hint when the actual quantity is below the minimum.

#### Scenario: Below minimum

- **WHEN** the actual quantity in a location is below its minimum
- **THEN** the system marks the item for refill

### Requirement: Default location from composition

The system SHALL derive an article's default location from the composition: a
location that mentions the base and is underfilled.

#### Scenario: Suggest a default location

- **WHEN** an article's base is underfilled in a location
- **THEN** that location is offered as the default location for storing

### Requirement: Consuming reduces quantity

The system SHALL reduce an article's quantity when it is consumed and SHALL
delete the article once no stock remains.

#### Scenario: Consume the last unit

- **WHEN** the last unit of a consumable is consumed
- **THEN** the article is deleted
