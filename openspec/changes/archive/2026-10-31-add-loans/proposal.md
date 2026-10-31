## Why

§20 loans the other way around (the organisation borrows from external
lenders). The reverse — a **private person borrows an article from the
organisation** — is not anchored anywhere, yet it is a common need (lending a
tent to a friend). The article stays the organisation's property; the loan
records who has it and until when.

## What Changes

- A `Loan` model: the article, the borrower (name + email), the period, an
  optional occasion, a status, and a token.
- The loan period is a **calendar entry** of a new type `loan`, so it shows in
  the calendar and the article's mini calendar.
- Create a loan from the article detail, list loans, and record the return.

## Capabilities

### New Capabilities

- `loans`: lending an article to an external person.

### Modified Capabilities

- `planning`: a `loan` calendar entry type.

## Impact

- New `loans` app; a new calendar entry type.
- **Deferred**: a borrower-facing link (needs §10 ShareLink); return reminders
  (a notification trigger); organisation-to-organisation loans.
