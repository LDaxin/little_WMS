## Context

§2 describes an article-level mini calendar. The `planning` app owns the
calendar; the article detail is rendered by `hub/modules/item.html`.

## Goals / Non-Goals

**Goals:**

- Show the article's occasions (packlist entries) and expiry date on its detail.

**Non-Goals:**

- Upcoming maintenance (no maintenance model yet).
- Past movements (already in the article's audit timeline).

## Decisions

### Decision 1: Terms built in the article view

`article/views.py` builds a sorted list of terms (date, label, optional url) and
passes it to the template; the module only renders.

### Decision 2: A hub module

The rendering lives in `hub/modules/articleCalendar.html`, included by
`item.html` when `articleCalendar` is set — consistent with the other modules.

## Risks / Trade-offs

- [Duplication with the audit timeline] → movements are intentionally left out;
  the mini calendar shows terms (occasions, expiry), not events.

## Migration Plan

- None.
