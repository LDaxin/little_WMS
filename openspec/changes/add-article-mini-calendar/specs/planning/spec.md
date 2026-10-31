## ADDED Requirements

### Requirement: Article-level mini calendar

The article detail SHALL show a mini calendar listing the article's dated terms:
the occasions the article is on the packlist of (each linking to its occasion)
and the article's expiry date when set. The terms SHALL be ordered by date.

#### Scenario: Occasions appear as terms

- **WHEN** an article is on an occasion's packlist
- **THEN** the article detail lists that occasion with its date, linking to the occasion

#### Scenario: Expiry date appears as a term

- **WHEN** an article has an expiry date
- **THEN** the article detail lists it

#### Scenario: No terms

- **WHEN** an article has no occasions and no expiry date
- **THEN** the mini calendar shows an empty state
