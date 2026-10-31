## ADDED Requirements

### Requirement: Custom dashboard widgets

The dashboard SHALL show a widget for each of the user's saved views marked to
appear on the dashboard, listing the view's articles with a link to apply it.

#### Scenario: A view on the dashboard

- **WHEN** a user marks a saved view to appear on the dashboard
- **THEN** the dashboard shows a widget with that view's articles

#### Scenario: Not marked

- **WHEN** a saved view is not marked
- **THEN** no widget is shown for it
