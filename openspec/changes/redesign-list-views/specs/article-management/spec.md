## ADDED Requirements

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
