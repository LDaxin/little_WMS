## ADDED Requirements

### Requirement: Web app manifest

The system SHALL serve a web app manifest at `/manifest.json` with the app name,
a standalone display, a theme color, and an icon, so the app can be installed.

#### Scenario: Manifest is served

- **WHEN** a browser requests `/manifest.json`
- **THEN** a JSON manifest with `display: standalone` is returned

### Requirement: Service worker

The system SHALL serve a service worker at `/sw.js` that caches the app shell
and static assets, so the app starts without network.

#### Scenario: Service worker is served

- **WHEN** a browser requests `/sw.js`
- **THEN** a JavaScript service worker is returned

#### Scenario: The app shell is cached

- **WHEN** the service worker installs
- **THEN** the app shell and static assets are cached
