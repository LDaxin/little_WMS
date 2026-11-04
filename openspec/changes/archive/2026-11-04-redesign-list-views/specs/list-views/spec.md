## ADDED Requirements

### Requirement: Table and card rendering

The system SHALL render a list as a table or as cards from the same query. The
result partial SHALL own the whole list (header and rows, or the card grid). The
user's per-device list-view setting SHALL decide the rendering (`table` or
`cards`); the device comes from the view-mode setting, or the client hint when
it is `auto`. The table/card toggle SHALL be available on every device.

#### Scenario: Desktop table

- **WHEN** the desktop list view is table
- **THEN** the list is rendered as a table

#### Scenario: Mobile cards

- **WHEN** the mobile list view is cards
- **THEN** the list is rendered as cards

#### Scenario: Auto follows the client

- **WHEN** the view mode is auto and the client reports a mobile viewport
- **THEN** the mobile list view is used

#### Scenario: Setting wins

- **WHEN** the user has set the desktop list view to table
- **THEN** the table is rendered regardless of the client hint

#### Scenario: Toggle on every device

- **WHEN** the user toggles the table/card switch
- **THEN** the list is rendered in the chosen mode on any device

### Requirement: Configurable columns

The system SHALL define the available columns per list type in code and SHALL
let the user choose which columns are shown and in which order. The selection
SHALL be data.

#### Scenario: Choose columns

- **WHEN** the user selects a different set of columns
- **THEN** the list shows exactly those columns

#### Scenario: Default columns

- **WHEN** the user has no selection
- **THEN** the list type's default columns are shown

### Requirement: View state

The system SHALL keep the view state (sort, columns, page) in URL parameters,
SHALL persist it in a Saved View, and SHALL fall back to the user's default when
no URL parameters are present.

#### Scenario: URL is the truth

- **WHEN** the user sorts or changes columns
- **THEN** the URL parameters reflect the new state

#### Scenario: Apply a saved view

- **WHEN** the user applies a saved view
- **THEN** its sort and columns are applied

### Requirement: Server-side sorting

The system SHALL sort the list server-side from a `sort` parameter, using the
sortable field declared by the column. A column SHALL toggle between ascending
and descending.

#### Scenario: Sort by a column

- **WHEN** the user clicks a sortable column header
- **THEN** the list is ordered by that column

#### Scenario: Toggle direction

- **WHEN** the user clicks the same header again
- **THEN** the order is reversed

### Requirement: Pagination

The system SHALL paginate the list server-side. Desktop SHALL show page numbers
that replace the list; mobile SHALL show a "load more" button that appends the
next page.

#### Scenario: Page numbers on desktop

- **WHEN** the user picks a page on desktop
- **THEN** the list shows that page

#### Scenario: Load more on mobile

- **WHEN** the user taps "load more" on mobile
- **THEN** the next page is appended to the list

### Requirement: Bulk selection

The system SHALL let the user select rows for bulk actions. Desktop SHALL use a
checkbox column; mobile SHALL use a selection mode entered by a button or a
long-press. "Select all" SHALL mean all matches, not only the loaded rows.

#### Scenario: Desktop selection

- **WHEN** the user checks rows on desktop
- **THEN** the bulk actions apply to the checked rows

#### Scenario: Mobile selection mode

- **WHEN** the user enters the selection mode on mobile
- **THEN** tapping a card selects it and a bulk action bar is shown

#### Scenario: Select all matches

- **WHEN** the user chooses "select all"
- **THEN** the bulk action applies to every matching row, not only the loaded ones

### Requirement: The list header stays visible

The system SHALL give the list its own scroll area so that only the rows scroll,
not the page, and SHALL keep the header visible while the rows scroll.

#### Scenario: Scroll the rows

- **WHEN** the list is longer than the viewport
- **THEN** the header stays visible and only the rows scroll

