# Article Management Specification

## Purpose

Manage articles: dynamic article types with type-specific fields, a shared
catalog (base) and individual instances, global and custom fields, codes, and
create/update/delete with audit logging.
## Requirements
### Requirement: Article types define their fields

The system SHALL let an administrator define article types, each with a
`field_config` for the global fields and a `custom_fields_schema` for
type-specific fields at base and article level.

#### Scenario: Type-specific fields

- **WHEN** an article type declares custom fields for the "base" or "article" level
- **THEN** only those fields are shown for articles of that type

#### Scenario: Container and merge/split are exclusive

- **WHEN** an article type is marked as both a container and merge/split
- **THEN** validation rejects it

### Requirement: Articles have a base and an instance

The system SHALL model an article as a shared `ArticleBase` (catalog data) plus
one or more `Article` instances, each with its own code and space.

#### Scenario: Create an article

- **WHEN** the user adds an article of a type
- **THEN** a base and an instance are created, the instance gets a code (`a0…`) and a space, and a "not stored" stock line is created

#### Scenario: Container space

- **WHEN** the article type is a container
- **THEN** the article's space is active so other articles can be stored in it

### Requirement: Global and custom fields

The system SHALL store global fields (condition, purchase value, purchase date,
expiry date, weight, note, consumable flag, unit) on every article and SHALL
validate custom field values against the type's schema.

#### Scenario: Invalid custom field

- **WHEN** a custom field value violates its schema (type, min/max, required)
- **THEN** the system rejects the save with a validation error

### Requirement: Codes are assigned and unique

The system SHALL assign each article a unique code and SHALL reject a code that
is already used.

#### Scenario: Use a pre-generated code

- **WHEN** the user provides a code that exists and is unused
- **THEN** the code is marked used and attached to the article

#### Scenario: Reject a used code

- **WHEN** the user provides a code that is already used
- **THEN** the system rejects the save with "code is already used"

### Requirement: Update and delete articles

The system SHALL update articles, log the changed fields, delete an article when
its quantity is set to zero, and soft-delete on explicit delete.

#### Scenario: Update logs a diff

- **WHEN** the user updates an article
- **THEN** the changed fields are written to the audit log

#### Scenario: Quantity zero deletes

- **WHEN** the user sets an article's quantity to zero
- **THEN** the article is deleted and the deletion is logged

#### Scenario: Delete an article

- **WHEN** the user deletes an article
- **THEN** the article is soft-deleted and the deletion is logged

### Requirement: Articles can be assigned to users

The system SHALL let a user assign an article to one or more users and SHALL
show the assignees on the article.

#### Scenario: Assign an article

- **WHEN** a user assigns an article to another user
- **THEN** the article is listed as assigned to that user

#### Scenario: Unassign an article

- **WHEN** a user removes an assignee from an article
- **THEN** the article is no longer assigned to that user

### Requirement: Article ownership

An article SHALL record whether it is owned by the organisation or borrowed from
an external lender, and whether lending it out requires confirmation.

#### Scenario: A borrowed article

- **WHEN** an article is borrowed from an external lender
- **THEN** its ownership is `borrowed`

#### Scenario: An owned article

- **WHEN** an article is created normally
- **THEN** its ownership is `owned`

### Requirement: All-articles list

The system SHALL provide `/article/` listing all articles across types, with the
quick search and the query builder.

#### Scenario: List all articles

- **WHEN** a user opens `/article/`
- **THEN** the articles of all types are listed

### Requirement: The all-articles list links to the detail page

The all-articles list SHALL link each row to the article's detail page and SHALL
show the article's type.

#### Scenario: Open an article from the all list

- **WHEN** the user opens the all-articles list and follows a row's link
- **THEN** the article's detail page is shown

#### Scenario: Type is shown

- **WHEN** the all-articles list is shown
- **THEN** each row shows the article's type

### Requirement: The article list is a grouped stock list

The article list SHALL show one row per (article, storage location). The first
row of an article SHALL show the article columns and the filtered total
quantity, marked when the filter hides locations (e.g. `2 (3 of 5 locations)`).
The location rows SHALL show only the location and the quantity. The group SHALL
be collapsible. Selection SHALL be per row. Pagination SHALL be per row; when a
group crosses a page boundary, the first row on the new page SHALL repeat the
article columns.

#### Scenario: Article with several locations

- **WHEN** an article sits in several locations
- **THEN** its first row shows the article columns and the total, and each further row shows a location and its quantity

#### Scenario: Filtered total

- **WHEN** a filter hides some of an article's locations
- **THEN** the total shows the filtered quantity and is marked as partial

#### Scenario: Collapse

- **WHEN** the user collapses an article's group
- **THEN** only its first row is shown

#### Scenario: Group across a page boundary

- **WHEN** an article's rows are split across two pages
- **THEN** the first row on the new page repeats the article columns

### Requirement: Article columns and cards

The article list SHALL offer the columns name, code, type, condition, location
and quantity by default, plus optional columns (expiry date, purchase value,
purchase date, weight, unit, tags, assignees, minimum stock, ownership, note).
The article card SHALL show image, name, code, type, location, quantity and a
condition badge; for several locations it SHALL show the total quantity and the
number of locations.

#### Scenario: Default columns

- **WHEN** the article list is shown with default columns
- **THEN** name, code, type, condition, location and quantity are shown

#### Scenario: Card with several locations

- **WHEN** an article with several locations is shown as a card
- **THEN** the card shows the total quantity and the number of locations

