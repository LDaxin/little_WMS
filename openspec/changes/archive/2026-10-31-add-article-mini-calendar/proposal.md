## Why

§2 describes an article-level mini calendar: each article's detail view shows
that article's dated terms, connecting the central calendar to individual
articles ("Where and when is this tent used?").

## What Changes

- The article detail shows a mini calendar listing the article's terms:
  - the occasions the article is on the packlist of (linked), and
  - its expiry date (for consumables).

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `planning`: add the article-level mini calendar.

## Impact

- `article/views.py` builds the terms; a new `hub/modules/articleCalendar.html`
  module renders them on the article detail.
- **Deferred**: upcoming maintenance (no maintenance model yet); past movements
  (already shown in the article's audit timeline).
