## ADDED Requirements

### Requirement: Borrow an article from an external lender

The system SHALL let a user record that the organisation borrows an article from
an external person or another organisation, with the lender, an optional
occasion, a period, and a status. The borrowed article SHALL be marked as not
owned by the organisation.

#### Scenario: Borrow from a person

- **WHEN** the user records a loan from an external person
- **THEN** a loan is created and the article is marked borrowed

#### Scenario: Borrow from an organisation

- **WHEN** the user records a loan from another organisation
- **THEN** the loan records the lending organisation

#### Scenario: Return a borrowed article

- **WHEN** the user records the return
- **THEN** the loan's status becomes returned

#### Scenario: Permission missing

- **WHEN** a user without `article.move_all` records a loan
- **THEN** the system responds with 403

### Requirement: Lending out (renamed)

The system SHALL keep the lending-out direction (the organisation lends an
article to an external person) under the name `Lending`.

#### Scenario: Lend out

- **WHEN** the user lends an article to a person
- **THEN** a lending is created
