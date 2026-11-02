## ADDED Requirements

### Requirement: Webhook channel

A notification rule SHALL support a webhook channel: an optional URL and an
optional secret. When the channel is set, the trigger command SHALL POST the
finding as JSON to the URL, with the secret in the `X-Webhook-Secret` header. A
failed POST SHALL be logged and SHALL NOT abort the command.

#### Scenario: Webhook fired

- **WHEN** a finding matches an active rule with a webhook URL
- **THEN** the finding is POSTed as JSON to that URL

#### Scenario: Secret sent

- **WHEN** the rule has a webhook secret
- **THEN** the request carries it in the `X-Webhook-Secret` header

#### Scenario: Webhook fails

- **WHEN** the webhook URL is unreachable
- **THEN** the failure is logged and the command continues

#### Scenario: No webhook

- **WHEN** the rule has no webhook URL
- **THEN** no webhook request is made
