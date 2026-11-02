## Why

§6 lists a webhook channel as part of the notification system: a rule can POST a
JSON payload to a URL, enabling Slack, Discord and custom integrations. The
notification system is otherwise built (in-app, email, rules, triggers), but the
webhook channel was never finished.

## What Changes

- `NotificationRule` gains `channel_webhook` (URL) and `webhook_secret`.
- A `notify_webhook` service POSTs the finding as JSON, with the secret in an
  `X-Webhook-Secret` header; a failed POST is logged, not fatal.
- The trigger command fires the webhook once per rule and finding when the
  channel is set.
- The rule form and list show the webhook channel.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `notification-rules`: a rule can deliver a finding to a webhook URL.

## Impact

- `notifications` app: model fields + migration, service, command, form, template.
- No new dependency (stdlib `urllib.request`).
