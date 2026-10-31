## Why

The loan offers (`LoanOffer` / `LoanOfferItem`) duplicate what saved views and
share links already do: a named list of articles shared via a capability URL.
Reusing §9/§10 removes the duplication.

## What Changes

- Remove `LoanOffer` and `LoanOfferItem`.
- An offer becomes a **saved view** shared via a **share link**.
- `ShareLink` gains `permissions` (default `["view"]`) and
  `requires_confirmation`; a link with the `borrow` permission lets a logged-in
  user borrow the view's articles (a loan, pending or active).
- Keep `OrganisationMembership` (shared pools) — there is no existing system for
  it; it lives in the `loans` capability.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `saved-views`: share links can allow borrowing.
- `loans`: offers are saved views + share links; shared pools; pending loans.

## Impact

- `loans` loses the offer models; `savedviews` gains link permissions.
