## Why

§6 lists notification triggers (expiry, maintenance due, low stock). The
notification center exists but nothing fills it automatically. The triggers
should be a separate layer, so later other consumers (email, webhook, dashboard
alerts, digests) can use the same findings.

## What Changes

- A `checks` layer that scans for due items and yields `Finding`s, independent of
  notifications.
- A `check_notifications` management command that turns findings into
  notifications via the central service.
- Triggers: `expiry_date_reached`, `maintenance_due`, `minimum_stock_undercut`.
- A `dedupe_key` on `Notification` so the same alert is not created repeatedly.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `notifications`: triggers that create notifications.

## Impact

- `Notification.dedupe_key` + migration; `notifications/checks.py`; a management
  command.
- **Deferred**: email / webhook delivery, digests, a configurable rules UI,
  scheduling (cron is an operational concern).
