## Why

§35 (GDPR) requires a user to be able to export their personal data and to have
their account deleted, with the activity logs anonymised (traceability stays,
the personal reference goes).

## What Changes

- A "my data" export: a JSON of the user's profile, activities, and loans.
- User deletion with anonymisation: the account and profile are removed, and the
  user's audit-log entries are anonymised.

## Capabilities

### New Capabilities

- `gdpr`: data export and deletion with anonymisation.

### Modified Capabilities

<!-- none -->

## Impact

- New views/urls in the `security` app.
- **Deferred**: the privacy-policy link and the registration consent checkbox;
  operator duties (not the system).
