## Context

§23 organisation requests: approving creates the organisation and an invitation,
but the link is not surfaced and there is no SMTP, so the requester cannot join.

## Goals / Non-Goals

**Goals:**

- Surface the invitation link after approval.

**Non-Goals:**

- Sending the invitation by email (needs SMTP, §30).
- Creating an account directly on approval (the requester registers via the link).

## Decisions

### Decision 1: Link the invitation to the request

`OrganisationRequest.invitation` (FK, nullable) is set on approval, so the
requests page can show the link for approved requests without guessing.

### Decision 2: Show the link with a copy button

The requests template shows the absolute invitation URL and a copy button,
reusing the clipboard pattern already used on the item page.

## Risks / Trade-offs

- [Manual sharing] → acceptable until SMTP (§30) exists.

## Migration Plan

- One nullable FK on `OrganisationRequest`.
