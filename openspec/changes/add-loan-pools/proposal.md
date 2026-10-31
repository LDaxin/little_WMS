## Why

§20 describes loan offers (a list of articles offered for loan, with a
confirmation step) and shared pools (an organisation that lends to member
organisations). The borrowing direction exists; the offers and pools do not.

## What Changes

- `LoanOffer` and `LoanOfferItem` models, with the confirmation resolution
  (item → offer → article).
- `OrganisationMembership` (a pool lends to member organisations).
- `Loan.status` gains `pending`: borrowing from an offer that requires
  confirmation creates a pending loan, confirmed by the lender.
- Views: create an offer, list offers, borrow from an offer, confirm a loan.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `loans`: loan offers and shared pools.

## Impact

- `loans` app gains the offer and membership models.
- **Deferred**: a full pool-management UI; enforcing `can_add`; cross-organisation
  visibility.
