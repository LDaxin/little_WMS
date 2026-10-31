# dashboard Specification

## Purpose
TBD - created by archiving change add-dashboard. Update Purpose after archive.
## Requirements
### Requirement: Dashboard

The system SHALL provide a dashboard page that shows widgets relevant to the
user, each gated by a permission: upcoming occasions, notifications, alerts,
quick actions, statistics, and recent activity. A widget SHALL only be shown
when the user holds its permission.

#### Scenario: Upcoming occasions widget

- **WHEN** a user with `occasion.view_all` opens the dashboard
- **THEN** the upcoming occasions are shown

#### Scenario: Alerts widget

- **WHEN** a user with `article.view_all` opens the dashboard
- **THEN** the current alerts (expiry, maintenance, low stock) are shown

#### Scenario: Permission gating

- **WHEN** a user lacks a widget's permission
- **THEN** that widget is not shown

#### Scenario: Requires login

- **WHEN** a visitor who is not logged in opens the dashboard
- **THEN** they are redirected to the login page

### Requirement: Custom dashboard widgets

The dashboard SHALL show a widget for each of the user's saved views marked to
appear on the dashboard, listing the view's articles with a link to apply it.

#### Scenario: A view on the dashboard

- **WHEN** a user marks a saved view to appear on the dashboard
- **THEN** the dashboard shows a widget with that view's articles

#### Scenario: Not marked

- **WHEN** a saved view is not marked
- **THEN** no widget is shown for it

