## Context

`ShareLink` (§10) shares a saved view and lets a logged-in user borrow the
organisation's articles (org-to-org). §20's friend scenario is the reverse: an
external person lends an item in, without an account. `hub.models.TokenisedModel`
provides the token + expiry base; `ArticleImage` provides the photo.

## Goals / Non-Goals

**Goals:**

- A capability link an organisation member creates for external lending.
- A public form that creates a borrowed article + loan + calendar entry.
- The external person sees the loan status.

**Non-Goals:**

- Account linking ("create an account to manage your loans").
- Reminder emails for account-less loans.
- Organisation-to-organisation loans and shared pools.

## Decisions

### Decision 1: A dedicated `LendLink` model

`LendLink` extends `TokenisedModel` (token + expiry) with `organisation`,
`label`, `is_active`, `single_use`, `used_count`, `password_hash`, `created_by`.
It is separate from `ShareLink` because it is not tied to a saved view.

### Decision 2: A dedicated "borrowed" article type

The lent item becomes an `Article` under a per-organisation `borrowed`
`ArticleType` (`get_or_create`), so the external person does not have to pick
from the organisation's types.

### Decision 3: Session-based status

After submitting, the loan id is stored in the session under the link, so
re-opening the link shows the loan status instead of the form.

## Risks / Trade-offs

- [Article name length] → `ArticleBase.name` is 20 chars; the form validates it.
- [Spam] → links are revocable and may expire; a password is optional.

## Migration Plan

- New table `loans_lendlink`; no data migration. Rollback: drop the table.
