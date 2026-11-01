## ADDED Requirements

### Requirement: Sidebar navigation

The system SHALL provide a vertical sidebar instead of the top navbar, with the
logo, quick navigation (dashboard, articles, storages, movement), notifications,
settings, roles (when permitted), logout, and the organisation switcher.

#### Scenario: Sidebar on every page

- **WHEN** an authenticated user opens any page
- **THEN** the sidebar is shown with the navigation and actions

#### Scenario: Content not covered

- **WHEN** the sidebar is shown
- **THEN** the content area is offset so the sidebar does not cover it

### Requirement: Responsive sidebar

The system SHALL show the sidebar as a narrow icon rail that expands on hover
(desktop) or via a toggle (mobile).

#### Scenario: Narrow rail

- **WHEN** the sidebar is not expanded
- **THEN** only the icons are shown

#### Scenario: Expand

- **WHEN** the sidebar is hovered (desktop) or the toggle is used (mobile)
- **THEN** the labels are shown

### Requirement: Sidebar settings

The system SHALL let a user choose the sidebar position (left/right), the icon
size, the text size, and the view mode (auto / always mobile / always desktop)
on the preferences page. Icon and text size SHALL be configurable separately for
desktop and mobile.

#### Scenario: Position

- **WHEN** a user chooses the right position
- **THEN** the sidebar is shown on the right

#### Scenario: View mode

- **WHEN** a user chooses "always mobile"
- **THEN** the mobile layout is used regardless of the viewport

#### Scenario: Icon size

- **WHEN** a user changes the icon size
- **THEN** the sidebar icons are shown at the chosen size

#### Scenario: Text size

- **WHEN** a user changes the text size
- **THEN** the whole app text (content and sidebar) is shown at the chosen size
