## ADDED Requirements

### Requirement: The detail modal is full-screen on mobile

The detail modal SHALL render full-screen on a mobile viewport and SHALL stay a
window on desktop.

#### Scenario: Full-screen on mobile

- **WHEN** the detail modal opens on a mobile viewport
- **THEN** it covers the full screen

#### Scenario: Window on desktop

- **WHEN** the detail modal opens on desktop
- **THEN** it renders as a window, not full-screen

## MODIFIED Requirements

### Requirement: Saving refreshes the list and closes the modal

After a successful save the detail view SHALL stay open and the field area SHALL
return to the read-only summary with the updated values; the list SHALL be
refreshed in the background. Closing the modal manually SHALL also refresh the
list, so the change is visible.

#### Scenario: Save keeps the detail open

- **WHEN** the user saves the detail form
- **THEN** the detail view stays open and the field area shows the read-only summary with the updated values

#### Scenario: List refreshed in the background

- **WHEN** the user saves the detail form
- **THEN** the list behind the detail is refreshed

#### Scenario: Manual close refreshes the list

- **WHEN** the user closes the modal manually
- **THEN** the list is refreshed
