## Context

§20 describes the organisation borrowing from external lenders. The previous
change built the reverse direction and used the name `Loan`; this change renames
it and adds the §20 direction.

## Goals / Non-Goals

**Goals:**

- Rename the lending-out model to `Lending`.
- `Article.ownership` + `loan_requires_confirmation`.
- A `Loan` (borrow in) with lender person/organisation, occasion, period, status.

**Non-Goals:**

- `LoanOffer` / `LoanOfferItem` (offer lists + confirmation resolution).
- `OrganisationMembership` (shared pools).
- The share-link friend scenario (§10).

## Decisions

### Decision 1: Rename `Loan` → `Lending`

§20 reserves `Loan` for the borrowing-in direction. The lending-out model
(previous change) becomes `Lending`, so the names match the spec.

### Decision 2: `Article.ownership`

`ownership` (`owned`/`borrowed`) and `loan_requires_confirmation` per §20. A
borrowed article behaves normally but is marked as not the organisation's
property.

### Decision 3: `Loan` (borrow in)

`lender_type` (person/organisation), `lender_name` (person), `lender_organisation`
(org), `borrower_organisation`, `occasion` (optional), `start_date`/`end_date`,
`status`, `notes`.

### Decision 4: Permission

Recording a loan requires `article.move_all`.

## Risks / Trade-offs

- [Rename] → `ki` is not live, so a plain rename migration is fine.

## Migration Plan

- Rename the model; add `Article.ownership`; add the `Loan` model.
