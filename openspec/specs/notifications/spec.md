# notifications Specification

## Purpose
TBD - created by archiving change add-notification-center. Update Purpose after archive.
## Requirements
### Requirement: Create notifications

The system SHALL let code create a notification for a user with a title, an
optional message, an optional link, and a trigger type. A central service SHALL
be the only way to create notifications.

#### Scenario: Notify a user

- **WHEN** code calls the notification service for a user
- **THEN** an unread notification is created for that user

#### Scenario: Notify by permission

- **WHEN** code notifies everyone holding a permission
- **THEN** each such user gets an unread notification

### Requirement: Notification center

The system SHALL show a bell with the unread count in the navigation, a dropdown
with the latest notifications, and a page listing all of the user's
notifications with a link and a read state.

#### Scenario: Unread badge

- **WHEN** a user has unread notifications
- **THEN** the bell shows the unread count

#### Scenario: List notifications

- **WHEN** the user opens the notification page
- **THEN** their notifications are listed with their link and read state

### Requirement: Mark notifications read

The system SHALL let a user mark a notification read or all notifications read.

#### Scenario: Mark one read

- **WHEN** the user marks a notification read
- **THEN** it is no longer unread

#### Scenario: Mark all read

- **WHEN** the user marks all notifications read
- **THEN** none of their notifications are unread

#### Scenario: Permission missing

- **WHEN** a user without `notification.view_all` opens the notification page
- **THEN** the system responds with 403

### Requirement: Notification triggers

The system SHALL provide a checks layer that scans for due items and yields
findings, independent of notifications, and a command that turns those findings
into notifications for the responsible roles. The triggers SHALL be
`expiry_date_reached`, `maintenance_due`, and `minimum_stock_undercut`.

#### Scenario: Expiry trigger

- **WHEN** an article expires within the threshold
- **THEN** a finding is produced and a notification is created for the responsible roles

#### Scenario: Maintenance trigger

- **WHEN** a maintenance entry is due
- **THEN** a finding is produced and a notification is created

#### Scenario: Low-stock trigger

- **WHEN** an article's stock is below its minimum
- **THEN** a finding is produced and a notification is created

#### Scenario: No duplicates

- **WHEN** the command runs again while a finding is still open
- **THEN** no second notification is created for the same finding

### Requirement: Notification emails

The system SHALL send an email when a notification is created for a user, using
the notification's title as the subject and its message and link as the body.
The email SHALL be subject to the recipient's verification and the
`notifications` category preference.

#### Scenario: Notify with email

- **WHEN** a notification is created for a user with a verified, subscribed address
- **THEN** an email is sent

#### Scenario: Opted out

- **WHEN** a notification is created for a user who opted out of `notifications`
- **THEN** the in-app notification is created but no email is sent

#### Scenario: Unverified

- **WHEN** a notification is created for a user whose address is not verified
- **THEN** the in-app notification is created but no email is sent

