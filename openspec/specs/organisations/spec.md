# Organisations Specification

## Purpose

Support multiple organisations: every object belongs to one organisation, a user
can be a member of several organisations with a different role in each, and all
work happens within the active organisation.

## Requirements

### Requirement: Objects belong to an organisation

The system SHALL assign every organisation-scoped object to exactly one
organisation, defaulting to the active organisation.

#### Scenario: New object uses the active organisation

- **WHEN** an object is created while an organisation is active
- **THEN** the object is assigned to that organisation

### Requirement: Membership

The system SHALL let a user belong to several organisations, with one membership
profile per organisation and a role per organisation.

#### Scenario: Multiple memberships

- **WHEN** a user is a member of two organisations
- **THEN** the user has two membership profiles, one per organisation

#### Scenario: Unique membership

- **WHEN** a membership for the same user and organisation already exists
- **THEN** a second one is rejected

### Requirement: Active organisation

The system SHALL keep the active organisation in the session, select it at login,
and let the user switch it.

#### Scenario: Single membership

- **WHEN** a user belongs to exactly one organisation
- **THEN** that organisation is used directly after login

#### Scenario: Multiple memberships

- **WHEN** a user belongs to several organisations
- **THEN** the user is asked which organisation to use

#### Scenario: Switch organisation

- **WHEN** the user switches to another organisation they belong to
- **THEN** the active organisation changes and the view updates

### Requirement: Queries are scoped to the active organisation

The system SHALL scope reads to the active organisation, so a user never sees
objects from another organisation.

#### Scenario: Isolation

- **WHEN** an organisation is active
- **THEN** queries return only objects of that organisation

#### Scenario: No active organisation

- **WHEN** no organisation is active (e.g. admin, shell, tests)
- **THEN** queries are not filtered
