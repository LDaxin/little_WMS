## ADDED Requirements

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
