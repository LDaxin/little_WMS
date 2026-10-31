## ADDED Requirements

### Requirement: Article ownership

An article SHALL record whether it is owned by the organisation or borrowed from
an external lender, and whether lending it out requires confirmation.

#### Scenario: A borrowed article

- **WHEN** an article is borrowed from an external lender
- **THEN** its ownership is `borrowed`

#### Scenario: An owned article

- **WHEN** an article is created normally
- **THEN** its ownership is `owned`
