## ADDED Requirements

### Requirement: Shared pools

The system SHALL let an organisation be a member of a pool (another
organisation), with `can_borrow` and `can_add` flags, so pool members can borrow
from the pool.

#### Scenario: A pool membership

- **WHEN** an organisation is added as a member of a pool
- **THEN** the membership records whether it may borrow and add

### Requirement: Pending loans

The system SHALL allow a loan to be `pending` until the lender confirms it, used
when borrowing requires confirmation.

#### Scenario: Pending then confirmed

- **WHEN** a loan requires confirmation
- **THEN** it is created pending and becomes active once confirmed
