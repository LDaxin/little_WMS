## ADDED Requirements

### Requirement: SMTP configuration from the environment

The system SHALL read the SMTP configuration (`EMAIL_HOST`, `EMAIL_PORT`,
`EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`,
`DEFAULT_FROM_EMAIL`) from environment variables, and SHALL consider email
configured only when `EMAIL_HOST` is set.

#### Scenario: SMTP configured

- **WHEN** `EMAIL_HOST` is set
- **THEN** the system sends mail through that SMTP server

#### Scenario: SMTP not configured

- **WHEN** `EMAIL_HOST` is not set
- **THEN** the system uses the console backend and reports email as not configured

### Requirement: Central mail service

The system SHALL send all mail through one central service. When email is not
configured the service SHALL log a warning and skip the message instead of
raising.

#### Scenario: Send when configured

- **WHEN** code calls the mail service with a recipient, subject, and body
- **THEN** the message is sent through the configured backend

#### Scenario: Skip when not configured

- **WHEN** email is not configured and code calls the mail service
- **THEN** a warning is logged, no message is sent, and no error is raised

### Requirement: Test email

The system SHALL let a superuser send a test email from the server settings page
and SHALL report whether it was sent or skipped.

#### Scenario: Send a test email

- **WHEN** a superuser triggers the test email
- **THEN** a test message is sent to their address and the result is shown

#### Scenario: Test email without configuration

- **WHEN** a superuser triggers the test email while email is not configured
- **THEN** the system reports that email is not configured and sends nothing
