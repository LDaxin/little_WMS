## ADDED Requirements

### Requirement: Scanning gives audible and haptic feedback

The system SHALL signal the outcome of a scan to the client and SHALL play a
short tone and vibrate on a successful scan, and a different tone and vibration
on an error. The user SHALL be able to turn sound and vibration off and set the
volume.

#### Scenario: Successful scan

- **WHEN** the user scans a known code
- **THEN** the client plays the success tone and vibrates

#### Scenario: Failed scan

- **WHEN** the user scans an unknown code
- **THEN** the client plays the error tone and vibrates differently

#### Scenario: Sound turned off

- **WHEN** the user has turned sound off
- **THEN** no tone is played

#### Scenario: Vibration turned off

- **WHEN** the user has turned vibration off
- **THEN** the device does not vibrate
