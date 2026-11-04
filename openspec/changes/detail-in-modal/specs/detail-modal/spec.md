## ADDED Requirements

### Requirement: Detail opens in a modal from the list

The list SHALL open an item's detail in a modal instead of navigating to the
detail page, when the user activates the detail trigger (the table's edit
button or a card). The list SHALL stay in place (filters, sort and scroll).

#### Scenario: Edit button opens the modal

- **WHEN** the user activates a row's edit button
- **THEN** the item detail opens in a modal on the list

#### Scenario: Card opens the modal

- **WHEN** the user clicks a card
- **THEN** the item detail opens in a modal on the list

#### Scenario: The list is not left

- **WHEN** the detail modal is open
- **THEN** the list behind it keeps its filters, sort and scroll position

### Requirement: The direct detail URL still renders the full page

Opening a detail URL directly SHALL render the full detail page (not the modal
fragment), so links and reloads keep working.

#### Scenario: Direct URL

- **WHEN** the user opens the detail URL directly
- **THEN** the full detail page is shown

### Requirement: Detail actions work in the modal

Every action on the detail view SHALL be usable inside the modal (edit and save,
store/remove, tags, images, assign, maintenance, floor plan).

#### Scenario: Edit and save in the modal

- **WHEN** the user edits a field in the modal and saves
- **THEN** the change is applied

#### Scenario: Store in the modal

- **WHEN** the user stores the item from the modal
- **THEN** the store action is applied inside the modal

### Requirement: Saving refreshes the list and closes the modal

After a successful save the modal SHALL close and the list SHALL reload, so the
change is visible.

#### Scenario: Save closes and reloads

- **WHEN** the user saves the detail form in the modal
- **THEN** the modal closes and the list shows the updated item
