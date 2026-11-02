## Context

`ShareLink` (§10) shares a saved view and lets a logged-in user borrow the
organisation's articles (org-to-org). §20's friend scenario is the reverse: an
external person lends items in, without an account. `hub.models.TokenisedModel`
provides the token + expiry base; `ArticleImage` provides the photo.

## Goals / Non-Goals

**Goals:**

- A capability link an organisation member creates for external lending.
- A public page where the external person manages a list of items.
- Deactivation removes the items and anonymises the lender's data.

**Non-Goals:**

- Account linking ("create an account to manage your loans").
- Reminder emails for account-less loans.
- Organisation-to-organisation loans and shared pools.

## Decisions

### Decision 1: A dedicated `LendLink` model

`LendLink` extends `TokenisedModel` (token + expiry) with `organisation`,
`label`, `lender_name`, `lender_email`, `is_active`, `password_hash`,
`created_by`. The lender's identity is stored on the link (entered once).

### Decision 2: `Loan.lend_link` links the items

Each lent item is a `Loan` with `lend_link` set, so the public page can list and
manage exactly the link's items.

### Decision 3: A dedicated "borrowed" article type

The lent item becomes an `Article` under a per-organisation `borrowed`
`ArticleType` (`get_or_create`), so the external person does not have to pick
from the organisation's types.

### Decision 4: Deactivation mirrors the GDPR user deletion

Deactivating a link soft-deletes the items' articles and loans and clears the
lender's name/email, like `security.views.deleteUser` anonymises a deleted user.

## Risks / Trade-offs

- [Article name length] → `ArticleBase.name` is 20 chars; the form validates it.
- [Spam] → links are deactivatable and may expire; a password is optional.

## Migration Plan

- New table `loans_lendlink`; `Loan` gains `lend_link`. Rollback: drop both.
