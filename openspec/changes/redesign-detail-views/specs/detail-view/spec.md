## ADDED Requirements

### Requirement: The detail view has a compact header

Each detail view SHALL show a compact header with only the object's identity
(small image, name, code, type) and the primary actions (Store/Move, Edit).
Editable values (quantity, condition, location, description, and the other form
fields) SHALL NOT be shown in the header; they SHALL live in the field area.

#### Scenario: Header shows identity and actions

- **WHEN** the detail view is open
- **THEN** the header shows the small image, name, code and type, plus the Store/Move and Edit actions

#### Scenario: Editable values are not in the header

- **WHEN** the detail view is open
- **THEN** quantity, condition and location are shown in the field area, not in the header

### Requirement: Detail sections are collapsible with count summaries

The detail view SHALL render the modules (stock, calendar, composition, tags,
assigned, images, history) as collapsible sections. Each section SHALL be
collapsed by default and its summary SHALL show a count when the module has
items.

#### Scenario: Sections are collapsed by default

- **WHEN** the detail view is open
- **THEN** every module section is collapsed

#### Scenario: Summary shows the count

- **WHEN** a module has items
- **THEN** its section summary shows the count (e.g. "Tags (3)")

#### Scenario: Empty module

- **WHEN** a module has no items
- **THEN** its section still exists and is readable as empty

### Requirement: Desktop layout toggles between accordion and tabs

On desktop the collapsible sections SHALL render as an accordion or as tabs.
The detail view SHALL offer a toggle for this. The choice SHALL be carried as a
`layout` URL parameter; without it the user setting `detail_layout_desktop`
SHALL apply, defaulting to `accordion`.

#### Scenario: Toggle switches the layout

- **WHEN** the user toggles the layout on desktop
- **THEN** the sections render as tabs or as an accordion accordingly

#### Scenario: URL parameter wins

- **WHEN** the detail URL carries `?layout=tabs`
- **THEN** the tabs layout is used regardless of the setting

#### Scenario: Setting is the default

- **WHEN** the detail URL has no `layout` parameter
- **THEN** the `detail_layout_desktop` setting decides the layout

#### Scenario: Invalid value falls back

- **WHEN** the `layout` parameter is neither `accordion` nor `tabs`
- **THEN** the `detail_layout_desktop` setting is used

### Requirement: Mobile always uses the accordion

On mobile the collapsible sections SHALL always render as an accordion and the
layout toggle SHALL NOT be shown.

#### Scenario: Mobile accordion

- **WHEN** the detail view is open on a mobile viewport
- **THEN** the sections render as an accordion

#### Scenario: No toggle on mobile

- **WHEN** the detail view is open on a mobile viewport
- **THEN** the accordion/tabs toggle is not shown

### Requirement: The detail view is read-only by default

The detail view SHALL render the field area as a read-only summary of label and
value by default, not as form inputs.

#### Scenario: Read-only summary is shown

- **WHEN** the detail view is open
- **THEN** the field area shows the values as read-only text, without inputs or a submit button

### Requirement: Edit swaps the field area in place

The detail view SHALL offer an Edit action that replaces the field area with the
form in place, and a Cancel action that swaps back to the read-only summary. The
header SHALL stay visible while editing. The form SHALL render the same fields
in the same order as the read-only summary.

#### Scenario: Edit opens the form in place

- **WHEN** the user activates Edit
- **THEN** the field area shows the form at the same position

#### Scenario: Cancel returns to read-only

- **WHEN** the user activates Cancel while editing
- **THEN** the read-only summary is shown again

#### Scenario: Header stays visible

- **WHEN** the user is editing
- **THEN** the header with identity and actions stays visible

#### Scenario: Same fields and order

- **WHEN** the user edits the fields
- **THEN** the form shows the same fields in the same order as the read-only summary

### Requirement: All shared detail views use the framework

The framework SHALL apply to every detail view that shares the detail templates:
Article, Storage, Location and Tag. The header content SHALL be configured per
type.

#### Scenario: Article and Storage detail

- **WHEN** an Article or Storage detail is open
- **THEN** it uses the compact header, collapsible sections and read/edit split

#### Scenario: Location and Tag detail

- **WHEN** a Location or Tag detail is open
- **THEN** it uses the same header and read/edit split with a header limited to identity
