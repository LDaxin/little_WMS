# Movement Specification

## Purpose

Move articles between storage locations and the "not stored" state: scan
articles into a buffer, pick a target location or container, confirm, and undo
mistakes. Every movement is written to the audit log and grouped in a movement
session.
## Requirements
### Requirement: Scanning codes fills the buffer and target

The system SHALL accept scanned codes and classify them: a storage code sets the
target location, an article code goes into the buffer. An unknown code SHALL
produce an error without changing the buffer or target.

#### Scenario: Scan a storage

- **WHEN** the user scans a storage code (`s0…`)
- **THEN** the storage becomes the target location for the next store

#### Scenario: Scan an article

- **WHEN** the user scans an article code (`a0…`) and no container default applies
- **THEN** the article is added to the buffer once, without duplicates

#### Scenario: Scan an unknown code

- **WHEN** the user scans a code that is neither a known storage nor a known article
- **THEN** the system shows an error and leaves the buffer and target unchanged

### Requirement: Containers become the target by default

The system SHALL treat a scanned article that can hold other articles (a
container with an active space) as the target location when no target is set,
and SHALL make this smart default reversible.

#### Scenario: Container scanned with an empty target

- **WHEN** the user scans a container and no target is set
- **THEN** the container becomes the target and the system marks it as a smart default

#### Scenario: Container scanned with a target already set

- **WHEN** the user scans a container while a target is already set
- **THEN** the container is added to the buffer instead

#### Scenario: Treat container as article

- **WHEN** the user chooses "Treat as article" on a smart-default target
- **THEN** the target is cleared and the container moves into the buffer

### Requirement: Storing moves buffered articles to the target

The system SHALL store all buffered articles into the resolved target location
in one atomic operation, and SHALL reject the store when the target is missing,
inactive, or would create a storage cycle or exceed the depth limit.

#### Scenario: Store buffered articles

- **WHEN** the user stores with a target set and a non-empty buffer
- **THEN** every buffered article is placed in the target and the buffer is cleared

#### Scenario: Store without a target

- **WHEN** the user stores without a valid target
- **THEN** the system shows an error and stores nothing

#### Scenario: Store into an inactive space

- **WHEN** the target space is inactive
- **THEN** the system rejects the store with "not active" and stores nothing

#### Scenario: Store a merge-split quantity

- **WHEN** the article type allows merge/split and the article has a "not stored" quantity
- **THEN** the stored amount is moved from the "not stored" line onto the target line, adding to any line already there

### Requirement: Removing takes articles out of storage

The system SHALL remove all buffered articles from storage back to their
"not stored" state.

#### Scenario: Remove buffered articles

- **WHEN** the user removes with a non-empty buffer
- **THEN** every buffered article's stored quantity moves to "not stored" and the buffer is cleared

### Requirement: Movement mode and buffer management

The system SHALL let the user switch between store and remove mode, clear the
buffer, remove a single article from the buffer, and set a buffered article as
the target.

#### Scenario: Switch mode

- **WHEN** the user switches between "Store" and "Remove"
- **THEN** the mode changes and the buffer and target are cleared

#### Scenario: Clear the buffer

- **WHEN** the user clears
- **THEN** the buffer and target are emptied

#### Scenario: Set a buffered article as target

- **WHEN** the user sets a buffered article as the target
- **THEN** the article is removed from the buffer and becomes the target

### Requirement: Movements are grouped in a session and can be undone

The system SHALL record every movement in the audit log linked to the user's
open movement session, SHALL show the session's entries, and SHALL let the user
undo the last action or one specific entry.

#### Scenario: Movement creates a session entry

- **WHEN** a store or remove succeeds
- **THEN** an audit entry is created and linked to the user's open session

#### Scenario: Undo the last action

- **WHEN** the user undoes the last action
- **THEN** the movement is reversed, the original entry is marked undone, and a counter entry is written

#### Scenario: Undo a specific entry

- **WHEN** the user undoes a specific session entry
- **THEN** that movement is reversed and the entry is marked undone

#### Scenario: Clear ends the session

- **WHEN** the user clears
- **THEN** the open movement session is ended

#### Scenario: Nothing to undo

- **WHEN** the user undoes with no undoable session entry
- **THEN** the system shows "Nothing to undo"

### Requirement: Store target field finds by code or name

The store-target field on an article SHALL find the target storage or container
by code OR by name (live suggestions), and SHALL offer the QR scanner.

#### Scenario: Search by name

- **WHEN** the user types a name in the store-target field
- **THEN** matching storages or containers are suggested and can be picked to store there

#### Scenario: Scan a target code

- **WHEN** the user scans a target code
- **THEN** the field accepts it and the article can be stored

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

### Requirement: The scanned article's image is shown

The system SHALL show the scanned article's primary image on the movement page
for visual confirmation, and SHALL let the user turn this off.

#### Scenario: Article with an image

- **WHEN** the user scans an article that has an image and the setting is on
- **THEN** the active card shows the article's primary image

#### Scenario: Article without an image

- **WHEN** the user scans an article that has no image
- **THEN** no image is shown

#### Scenario: Image turned off

- **WHEN** the user has turned the image off
- **THEN** no image is shown

