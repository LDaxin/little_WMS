## ADDED Requirements

### Requirement: Mobile list controls are thumb-reachable

In the mobile layout the list pages SHALL place the search bar and the control
bar (columns, table/cards toggle, select, select all) below the list and SHALL
keep them visible (pinned) while the list scrolls. The search bar SHALL be the
bottom-most element, the control bar directly above it. This SHALL apply to the
table and the card mode and to both the per-type and the "all" lists.

#### Scenario: Search and controls below the list

- **WHEN** a mobile user opens a list page
- **THEN** the search bar is at the bottom and the control bar directly above it, below the list

#### Scenario: Controls stay visible while scrolling

- **WHEN** the mobile user scrolls the list
- **THEN** the search bar and the control bar remain visible at the bottom

#### Scenario: Applies to both list modes

- **WHEN** the mobile list is shown as a table or as cards
- **THEN** the search bar and the control bar are placed below the list in both cases

### Requirement: Advanced search trigger with the search field

On the article list the advanced-search trigger SHALL sit in the search field
row, next to the QR button, in the mobile and the desktop layout.

#### Scenario: Trigger next to the QR button

- **WHEN** the article list is shown (mobile or desktop)
- **THEN** the advanced-search trigger is in the search field row, next to the QR button

### Requirement: Advanced search panel direction

The advanced-search panel SHALL open upward in the mobile layout and downward in
the desktop layout.

#### Scenario: Opens upward on mobile

- **WHEN** a mobile user opens the advanced-search panel
- **THEN** the panel opens upward from the trigger

#### Scenario: Opens downward on desktop

- **WHEN** a desktop user opens the advanced-search panel
- **THEN** the panel opens downward from the trigger

### Requirement: Scanner panel above the list

The QR scanner panel SHALL open above the list, independent of where the search
bar sits.

#### Scenario: Scanner opens above the list on mobile

- **WHEN** a mobile user opens the QR scanner
- **THEN** the scanner panel is shown above the list

#### Scenario: Scanner opens above the list on desktop

- **WHEN** a desktop user opens the QR scanner
- **THEN** the scanner panel is shown above the list

### Requirement: Mobile controls follow the sidebar side

In the mobile layout the system SHALL align the control bar and the search-field
buttons (QR, advanced) to the side of the sidebar — a left sidebar puts them on
the left, a right sidebar on the right — so a left-handed user reaches them with
the thumb. This SHALL follow the existing per-device sidebar position; no
separate setting is introduced.

#### Scenario: Right sidebar

- **WHEN** the mobile sidebar is on the right
- **THEN** the control bar and the search-field buttons are aligned to the right

#### Scenario: Left sidebar

- **WHEN** the mobile sidebar is on the left
- **THEN** the control bar and the search-field buttons are aligned to the left

#### Scenario: Desktop unchanged

- **WHEN** the desktop layout is shown
- **THEN** the control placement does not follow the sidebar side

