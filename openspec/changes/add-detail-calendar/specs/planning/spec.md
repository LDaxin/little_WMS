## MODIFIED Requirements

### Requirement: Article-level mini calendar

The article detail SHALL show the article's dated terms in the detail calendar
(§ detail-calendar): the occasions the article is on the packlist of (each
linking to its occasion), its maintenance entries, its loan periods, and its
expiry date when set. The terms SHALL be available both as a month grid and as a
list ordered by date.

#### Scenario: Occasions appear as terms

- **WHEN** an article is on an occasion's packlist
- **THEN** the article detail shows that occasion as a term, linking to the occasion

#### Scenario: Expiry date appears as a term

- **WHEN** an article has an expiry date
- **THEN** the article detail shows it

#### Scenario: No terms

- **WHEN** an article has no occasions, no maintenance, no loans and no expiry date
- **THEN** the calendar shows an empty state
