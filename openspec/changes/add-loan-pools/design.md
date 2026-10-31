## Context

§20 describes loan offers and shared pools. The borrowing direction exists; this
change adds the offers and pools.

## Goals / Non-Goals

**Goals:**

- `LoanOffer` / `LoanOfferItem` with the confirmation resolution.
- `OrganisationMembership` (shared pools).
- A `pending` loan status and the confirm step.

**Non-Goals:**

- A full pool-management UI; enforcing `can_add`.
- Cross-organisation visibility.

## Decisions

### Decision 1: Offers as a named list

`LoanOffer` (lender_organisation, name, requires_confirmation) with
`LoanOfferItem` (offer, article, requires_confirmation nullable).

### Decision 2: Confirmation resolution

`LoanOfferItem.requires_confirmation` → `LoanOffer.requires_confirmation` →
`Article.loan_requires_confirmation`.

### Decision 3: `pending` status

Borrowing from an offer that requires confirmation creates a `pending` loan;
the lender confirms it to `active`.

### Decision 4: Pools reuse Organisation

A pool is an organisation that lends; `OrganisationMembership` links a pool to
its members with `can_borrow` / `can_add`.

## Risks / Trade-offs

- [No pool UI yet] → memberships are managed via the admin for now.

## Migration Plan

- New models; a new `Loan.status` choice.
