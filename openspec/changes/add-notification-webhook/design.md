## Context

`NotificationRule` already carries the in-app and email channels; the trigger
command (`check_notifications`) resolves recipients from the active rules and
creates notifications. The webhook is a third channel: it does not target users
but an external URL, so it fires once per rule and finding, not per recipient.
`notifications/checks.py` already notes that other consumers (email, webhook,
dashboard) can reuse the same findings.

## Goals / Non-Goals

**Goals:**

- A rule can POST a finding as JSON to a webhook URL.
- An optional secret is sent so the receiver can verify the call.
- A failing webhook never breaks the trigger command.

**Non-Goals:**

- HMAC request signing (a shared-secret header is enough for now).
- Retries or delivery tracking.
- Per-user webhooks (the webhook is per rule, like the other channels).

## Decisions

### Decision 1: `channel_webhook` + `webhook_secret` on the rule

Both are optional; an empty URL means the channel is off. The secret is sent as
the `X-Webhook-Secret` header when set.

### Decision 2: stdlib `urllib.request`

No new dependency. `notify_webhook` builds a JSON body, POSTs it with a short
timeout, and returns whether it succeeded. Errors are caught and logged.

### Decision 3: Fire once per rule and finding

The webhook is not tied to recipients, so the command calls it once per matching
rule after (or instead of) the per-user notifications.

## Risks / Trade-offs

- [Blocking call] → a short timeout bounds the delay; a slow receiver can slow
  the command. Acceptable for a periodic command.
- [No retry] → a missed webhook is lost; the in-app/email channels remain the
  reliable path.

## Migration Plan

- Add two columns to `notifications_notificationrule`. Rollback: drop them.
