## ADDED Requirements

### Requirement: German language

The system SHALL offer German in addition to English, selectable per user.

#### Scenario: German available

- **WHEN** the available languages are listed
- **THEN** German and English are offered

#### Scenario: German selected

- **WHEN** a user selects German
- **THEN** the core UI is shown in German

### Requirement: Translated core UI

The system SHALL translate the core UI (navigation, login, hub, dashboard,
notifications, preferences, server settings, organisation pages, import, and the
common modules) to German.

#### Scenario: Navigation in German

- **WHEN** the language is German
- **THEN** the navigation and the core pages are shown in German

#### Scenario: Fallback

- **WHEN** a string has no German translation
- **THEN** the English string is shown
