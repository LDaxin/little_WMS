## ADDED Requirements

### Requirement: Translated remaining UI

The system SHALL translate the remaining UI (article, storage, movement,
occasion, planning, loans, reports, saved views, query builder, export,
onboarding, and the remaining modules) to German.

#### Scenario: Remaining pages in German

- **WHEN** the language is German
- **THEN** the remaining pages and their form labels are shown in German

#### Scenario: Fallback

- **WHEN** a string has no German translation
- **THEN** the English string is shown
