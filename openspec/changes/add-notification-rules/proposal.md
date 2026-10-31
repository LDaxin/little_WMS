## Why

§6 lists configurable notifications. The triggers are hardcoded: every finding
notifies the `article_view_all` role in-app. Admins cannot choose recipients,
thresholds, or channels.

## What Changes

- A `NotificationRule` per organisation and trigger type: active flag, a
  threshold, recipients (roles and individual users), and channels (in-app,
  email).
- `check_notifications` resolves recipients from the active rules; when no rule
  exists for a trigger it keeps the current default (the `article_view_all`
  role, in-app).
- A rules page to list, add, edit, and delete rules.

## Capabilities

### New Capabilities

- `notification-rules`: configurable notification rules (recipients, threshold,
  channels).

### Modified Capabilities

- `notifications`: the trigger command uses the configured rules.

## Impact

- `notifications` (model, command, views, urls, templates), `notify()` gains an
  email flag, tests.
- **Deferred**: `notify_responsible`, digests (daily/weekly), webhooks,
  editable email templates.
