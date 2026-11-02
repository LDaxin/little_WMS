## Why

§20 describes a "friend scenario": a private person lends an item to the
organisation via a link, without an account. The existing share link only lets a
logged-in user borrow the organisation's articles (org-to-org); there is no way
for an external person to lend something in.

## What Changes

- New `LendLink` model: a capability URL an organisation member creates so an
  external person can lend an item.
- A public form (`/lend/<token>/`): item name, description, period, optional
  photo.
- Submitting creates a borrowed article, a `Loan` (direction `in`, party type
  `person`) and a `loan` calendar entry; the friend sees the loan status.
- Organisation members create/revoke lend links from the loans page.

## Capabilities

### New Capabilities

- `lend-links`: a capability URL for an external person to lend an item to the
  organisation.

### Modified Capabilities

<!-- none -->

## Impact

- `loans` app: new model, views, urls, templates; migration.
- Reuses `hub.models.TokenisedModel` and `ArticleImage`.
