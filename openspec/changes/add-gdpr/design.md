## Context

§35 (GDPR) requires data export and deletion with anonymisation. The audit log
already stores the acting user; anonymising means clearing that reference.

## Goals / Non-Goals

**Goals:**

- A JSON export of the user's data.
- Deletion with anonymisation of the audit log.

**Non-Goals:**

- The privacy-policy link and the registration consent checkbox.
- Operator duties (not the system).

## Decisions

### Decision 1: Export as JSON

`/my-data/` returns a JSON with the profile, the user's audit-log entries, and
their loans.

### Decision 2: Anonymise by clearing the user reference

The audit log's `user` FK is `SET_NULL`; deleting a user clears it, so the log
stays without the personal reference (shown as "Deleted user").

### Decision 3: Permission

Deleting a user requires `user.deactivate_all`.

## Risks / Trade-offs

- [Deletion is destructive] → it is an explicit admin action.

## Migration Plan

- None.
