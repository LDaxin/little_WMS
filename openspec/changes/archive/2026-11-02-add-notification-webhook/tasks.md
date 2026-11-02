## 1. Model

- [x] 1.1 `NotificationRule.channel_webhook`, `webhook_secret`
- [x] 1.2 Migration

## 2. Delivery

- [x] 2.1 `notify_webhook` service (JSON POST, secret header, errors logged)
- [x] 2.2 Command fires the webhook per rule and finding

## 3. UI

- [x] 3.1 Rule form includes the webhook fields
- [x] 3.2 Rule list shows the webhook channel

## 4. Tests

- [x] 4.1 Webhook POST with payload and secret (mocked)
- [x] 4.2 Failing webhook does not break the command
- [x] 4.3 Rule form saves the webhook fields

## 5. Verify

- [x] 5.1 Full suite green in Docker
- [x] 5.2 Rebuild + restart
