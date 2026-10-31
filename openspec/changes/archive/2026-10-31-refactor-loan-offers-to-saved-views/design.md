## Context

The loan offers duplicate saved views + share links. This change removes them
and reuses §9/§10.

## Goals / Non-Goals

**Goals:**

- Remove `LoanOffer` / `LoanOfferItem`.
- Share links carry permissions and a confirmation flag; borrowing via a link.

**Non-Goals:**

- A pool-management UI (memberships stay via the admin).

## Decisions

### Decision 1: An offer is a saved view + share link

The saved view's query selects the articles; the share link is the capability
URL. No new offer models.

### Decision 2: Link permissions

`ShareLink.permissions` (JSON, default `["view"]`); `borrow` enables the borrow
action. `requires_confirmation` decides pending vs active.

### Decision 3: Borrowing needs a logged-in user

A loan needs a borrower organisation, so borrowing via a link requires login;
anonymous visitors can still view.

## Risks / Trade-offs

- [Removing models] → `ki` is not live, so a plain drop migration is fine.

## Migration Plan

- Drop the offer models; add the link fields.
