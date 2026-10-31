# i18n Specification

## Purpose
TBD - created by archiving change add-i18n-preparation. Update Purpose after archive.
## Requirements
### Requirement: Language configuration

The system SHALL define the available languages and a locale path, and SHALL
enable locale middleware. Only English SHALL be available for now.

#### Scenario: English only

- **WHEN** the available languages are listed
- **THEN** English is the only one

### Requirement: Per-user language

The system SHALL store a language per user, defaulting to English, and SHALL
activate it for that user's requests.

#### Scenario: Default language

- **WHEN** a user has no language set
- **THEN** English is used

#### Scenario: User language wins

- **WHEN** a user has a language set
- **THEN** their requests use that language, regardless of the browser's preference

### Requirement: Language selector

The system SHALL let a user choose their language on the preferences page.

#### Scenario: Choose a language

- **WHEN** a user selects a language and saves
- **THEN** the preference is stored and used for their requests

### Requirement: Translatable import strings

The import service and templates SHALL mark their user-facing strings for
translation.

#### Scenario: Marked for translation

- **WHEN** the import strings are extracted
- **THEN** they are found in the message catalogue

