## Why

§20 describes the organisation **borrowing** an article from an external person
or another organisation. The previous change built the reverse direction (the
organisation lends out), which reused the name `Loan`. To match §20, the
lending-out model is renamed to `Lending`, and the borrowing-in direction is
added.

## What Changes

- Rename `loans.Loan` to `loans.Lending` (the organisation lends out).
- `Article.ownership` (`owned` / `borrowed`) and `loan_requires_confirmation`.
- A new `loans.Loan` (the organisation borrows in) with a lender (person or
  organisation), an optional occasion, a period, and a status.
- Create / list / return for the borrowing direction.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `loans`: the borrowing-in direction and the `Lending` rename.
- `article-management`: article ownership.

## Impact

- `loans` app (rename + new model); `article` gets `ownership`.
- **Deferred**: `LoanOffer` / `LoanOfferItem` (offer lists + confirmation
  resolution); `OrganisationMembership` (shared pools); the share-link friend
  scenario (§10).
