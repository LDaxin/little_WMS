## Context

§20 loans the other way around. This change adds the reverse: a private person
borrows an article from the organisation, with the period as a calendar entry.

## Goals / Non-Goals

**Goals:**

- A `Loan` model with borrower name/email, period, status, optional occasion.
- The period as a `loan` calendar entry (shows in the calendar + mini calendar).
- Create / list / return.

**Non-Goals:**

- A borrower-facing link (needs §10 ShareLink).
- Return reminders (a notification trigger).
- Organisation-to-organisation loans.

## Decisions

### Decision 1: A `loans` app

Loans are a distinct domain; a dedicated app keeps the model, views, and
templates together.

### Decision 2: The period is a `CalendarEntry`

`Loan.calendar_entry` (OneToOne) is a `CalendarEntry` of type `loan`, carrying
the article and the start/end dates. This reuses the calendar and the article
mini calendar for free.

### Decision 3: Borrower by name + email

`borrower_name` (required) and `borrower_email` (optional, for later reminders).
No account is needed.

### Decision 4: Permission

Creating a loan requires `article.move_all` (it moves the article out).

## Risks / Trade-offs

- [No borrower link yet] → the organisation records the return for now.

## Migration Plan

- New app with an initial migration; a new calendar entry type (a choice, no
  schema change).
