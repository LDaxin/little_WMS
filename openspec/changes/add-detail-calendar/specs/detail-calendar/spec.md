## ADDED Requirements

### Requirement: The detail view has a calendar module with a grid/list switch

The detail view SHALL show the object's dated terms in a calendar module. The
module SHALL offer a switch between a month grid and a list; the chosen view
SHALL be a per-user setting. The list SHALL show the terms ordered by date.

#### Scenario: Switch between grid and list

- **WHEN** the user switches the module
- **THEN** the terms are shown as a month grid or as a list accordingly

#### Scenario: The chosen view is remembered

- **WHEN** the user chose the list view and opens the detail again
- **THEN** the module opens in the list view

### Requirement: The month grid shows ranges as bars and single days as dots

The month grid SHALL render a term that spans several days as a bar across its
days, continuing across week and month boundaries, and a single-day term as a
dot in its day cell. Bars and dots SHALL be coloured by the term's type and the
module SHALL show a legend. Today SHALL be highlighted and weeks SHALL be
visually separated.

#### Scenario: A range is a bar

- **WHEN** an article has a term from the 1st to the 14th
- **THEN** the grid shows a bar across those days

#### Scenario: A single day is a dot

- **WHEN** an article has a one-day term
- **THEN** the grid shows a dot in that day's cell

#### Scenario: Colours by type

- **WHEN** the grid shows terms of different types
- **THEN** each type has its own colour and the legend names them

### Requirement: The calendar scrolls through months and lazy-loads neighbours

The calendar module SHALL show the months in a scrollable area and SHALL load the
neighbouring months automatically as the user scrolls in either direction. The
month header SHALL stay visible while scrolling.

#### Scenario: Scrolling down loads the next month

- **WHEN** the user scrolls the calendar to the end of the shown months
- **THEN** the next month is loaded and appended

#### Scenario: Scrolling up loads the previous month

- **WHEN** the user scrolls the calendar to the start of the shown months
- **THEN** the previous month is loaded and prepended

### Requirement: A term is created by selecting a period in the grid

The user SHALL create a term by tapping days in the grid: the first tap on a
free day starts the selection, a second tap on the same day selects a single
day, and a tap on another day selects the range between the two days (the
earlier day is the start). The selection SHALL be cancellable with an × and by
tapping outside the grid. When the period is chosen the system SHALL check for
conflicts.

#### Scenario: Single-day selection

- **WHEN** the user taps a free day and then the same day again
- **THEN** a single-day period is selected

#### Scenario: Range selection

- **WHEN** the user taps a free day and then another day
- **THEN** the range between the two days is selected, starting at the earlier day

#### Scenario: Cancelling the selection

- **WHEN** the user taps the × or outside the grid
- **THEN** the selection is cleared

### Requirement: Conflicts are reported and free periods ask for an action

When the selected period overlaps an existing term the system SHALL NOT create a
term and SHALL show the conflicting terms in a popup. When the period is free
the system SHALL ask which action to perform (maintenance, lend, borrow) and open
the matching form in a popup, pre-filled with the period's dates.

#### Scenario: Overlapping period

- **WHEN** the selected period overlaps an existing term
- **THEN** a popup lists the conflicting term(s) and no term is created

#### Scenario: Free period asks for the action

- **WHEN** the selected period is free
- **THEN** a popup offers maintenance, lend or borrow

#### Scenario: The form is pre-filled

- **WHEN** the user picks an action
- **THEN** its form opens with the selected start and end dates

### Requirement: A term can be previewed, opened, edited and deleted

Tapping a day with an existing term SHALL show a preview of that day's terms;
tapping again SHALL open the term in a popup. The popup SHALL let the user edit
and delete a maintenance or loan term's title and dates. An occasion term SHALL
only link to its occasion; the expiry date SHALL be shown with a link to the
article.

#### Scenario: Preview then open

- **WHEN** the user taps a day with a term and then taps again
- **THEN** the term opens in a popup

#### Scenario: Editing a term

- **WHEN** the user changes a maintenance or loan term's title or dates in the popup
- **THEN** the calendar entry is updated and the grid reflects it

#### Scenario: Deleting a term

- **WHEN** the user deletes a maintenance or loan term in the popup
- **THEN** the calendar entry is removed and the grid reflects it

#### Scenario: Occasion links to its page

- **WHEN** the opened term is an occasion
- **THEN** the popup links to the occasion's detail page
