# query-builder Specification

## Purpose
TBD - created by archiving change add-query-builder. Update Purpose after archive.
## Requirements
### Requirement: Query parser

The system SHALL translate a JSON query (AND/OR groups, nested, optionally
negated, and condition rows) into Django `Q` objects, allowing only whitelisted
fields and operators per field type.

#### Scenario: AND of conditions

- **WHEN** a query has two conditions in an AND group
- **THEN** the result is the AND of both

#### Scenario: Nested OR group

- **WHEN** a query has an OR group inside an AND group
- **THEN** the result is the AND of the outer conditions and the OR of the inner ones

#### Scenario: Negated group

- **WHEN** a group is negated
- **THEN** the result is the negation of the group

#### Scenario: Unknown field or operator

- **WHEN** a query uses a field or operator that is not whitelisted
- **THEN** the parser raises an error

### Requirement: Query builder on the article list

The article list SHALL offer an advanced query builder that builds the JSON
query and applies it to the list.

#### Scenario: Apply a query

- **WHEN** the user builds a query and applies it
- **THEN** the article list shows only the matching articles

