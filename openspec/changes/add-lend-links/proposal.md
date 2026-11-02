## Why

§20 describes a "friend scenario": a private person lends items to the
organisation via a link, without an account. The existing share link only lets a
logged-in user borrow the organisation's articles (org-to-org); there is no way
for an external person to lend something in.

## What Changes

- New `LendLink` model: a capability URL an organisation member creates so an
  external person can lend items. The link stays valid until deactivated or
  expired.
- A public page (`/lend/<token>/`): the external person enters their name and
  email once, then manages a list of items (add, edit name/description/period,
  delete).
- Each item creates a borrowed article, a `Loan` (direction `in`, party type
  `person`) and a `loan` calendar entry.
- Deactivating a link removes its items and anonymises the lender's data.
- Organisation members create/deactivate lend links from the loans page.

## Capabilities

### New Capabilities

- `lend-links`: a capability URL for an external person to lend items to the
  organisation.

### Modified Capabilities

<!-- none -->

## Impact

- `loans` app: new model, `Loan.lend_link`, views, urls, templates; migration.
- Reuses `hub.models.TokenisedModel` and `ArticleImage`.
