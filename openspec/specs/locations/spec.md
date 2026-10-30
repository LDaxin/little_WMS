# Locations Specification

## Purpose

Manage locations (addresses) that storages can be assigned to: free-form address
lines plus optional structured fields, a code, and search.

## Requirements

### Requirement: Locations with addresses

The system SHALL let the user create locations with free-form address lines and
optional structured fields (postal code, city, state, country).

#### Scenario: Create a location

- **WHEN** the user adds a location
- **THEN** a location with its address fields and a code is created

#### Scenario: Update a location

- **WHEN** the user updates a location
- **THEN** the changed address fields are saved

### Requirement: Search locations

The system SHALL let the user search locations by address line, city, or code.

#### Scenario: Search by city

- **WHEN** the user searches for a city
- **THEN** the matching locations are listed

### Requirement: Delete locations

The system SHALL soft-delete a location.

#### Scenario: Delete a location

- **WHEN** the user deletes a location
- **THEN** the location is soft-deleted
