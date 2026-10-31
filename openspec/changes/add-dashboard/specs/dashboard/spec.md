## ADDED Requirements

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
