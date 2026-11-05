## ADDED Requirements

### Requirement: The detail view has a header with identity and summary

Each detail view SHALL show a header with the object's identity and a short
read-only summary. For an article the header shows the image, the name
(prominent), the type, the condition badge, the tags, the total quantity with
its unit, the storage locations and the code. The quantity SHALL be omitted
when it is 1. When the article is stored in exactly one location, that
location's name SHALL be shown instead of a location count. The header SHALL
NOT be the editing surface: editable values remain in the field area.

#### Scenario: Header shows identity and summary

- **WHEN** an article detail view is open
- **THEN** the header shows the image, the name, the type, the condition badge, the tags, the total quantity with unit, the storage locations and the code

#### Scenario: Quantity of one is hidden

- **WHEN** the article's total quantity is 1
- **THEN** the header does not show the quantity

#### Scenario: A single storage location is shown by name

- **WHEN** the article is stored in exactly one location
- **THEN** the header shows that location's name instead of a location count

#### Scenario: Header shows the actions

- **WHEN** the detail view is open
- **THEN** the header shows the actions (copy link, open, and per type floor plan / store / edit) in a row

#### Scenario: Editable values remain in the field area

- **WHEN** the user wants to change the quantity or the condition
- **THEN** the change happens in the field area, not in the header

#### Scenario: Types without the extra fields

- **WHEN** a Storage, Location or Tag detail view is open
- **THEN** the header shows only the fields that type has (identity and code), not an empty condition or quantity row

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

### Requirement: The field area uses one row layout for read and edit

The field area SHALL render each field as a row with the label in a left column
and the value (read) or the input (edit) in a right column. The read-only
summary and the form SHALL use the same row layout, so the view does not change
when entering edit. Inputs SHALL use a subtle border; checkboxes SHALL render as
a checkbox/switch and selects as selects. The summary SHALL show choice labels,
a check for a true boolean and a dash for an empty value.

#### Scenario: Same row layout in read and edit

- **WHEN** the user enters edit
- **THEN** each field keeps its label column and its value/input column position

#### Scenario: Inputs are not Bootstrap input-groups

- **WHEN** the user edits
- **THEN** each input has a subtle border, without an attached label box or a floating label

#### Scenario: Read-only values are human-readable

- **WHEN** the summary shows a choice, a boolean or an empty value
- **THEN** it shows the choice's label, a check or dash for the boolean, or a dash for the empty value

### Requirement: The header image opens a lightbox

When the object has images, tapping the header image SHALL open a full-screen
lightbox. The lightbox SHALL show the images large and allow scrolling sideways
between them. Each image SHALL offer a star that sets it as the primary image;
setting it SHALL update the header image and the image section. Without an image
the header shows the placeholder and no lightbox is rendered.

#### Scenario: Opening the lightbox

- **WHEN** the user taps the header image
- **THEN** a full-screen lightbox opens, positioned at the primary image

#### Scenario: Scrolling between images

- **WHEN** the lightbox is open
- **THEN** the user can scroll sideways through all of the object's images

#### Scenario: Setting the primary image

- **WHEN** the user taps the star on an image in the lightbox
- **THEN** that image becomes primary and the header image updates to it

#### Scenario: No image

- **WHEN** the object has no image
- **THEN** the header shows the placeholder and no lightbox exists

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
