## Context

The detail view's calendar module (`hub/modules/articleCalendar.html`) renders
the article's terms as a flat list plus three inline forms. The terms come from
`_article_terms`: occasions (via the article's packlist), maintenance entries,
loan entries, and the article's expiry date. Every term except the expiry date
is a `planning.CalendarEntry` row; occasions and loans are 1:1 specializations
of an entry. The detail-view redesign already gives the module a collapsible
section and a per-user setting pattern (`detail_layout_desktop`).

## Goals / Non-Goals

**Goals:**

- A month-grid mini calendar: range bars, single-day dots, colours per type,
  legend, today/week highlighting.
- A scrollable month view that lazy-loads the neighbouring months.
- Create a term by selecting a period, with a conflict check and an action
  choice (maintenance / lend / borrow).
- Preview and open a term, and edit/delete the underlying entry.
- A per-user switch between the calendar grid and the list.

**Non-Goals:**

- A database constraint preventing overlapping terms and adding times to entries
  (separate change).
- Changing the loan/occasion workflows or merging the models.
- A reusable generic calendar component outside the detail view.

## Decisions

### Decision 1: One presentation built from `CalendarEntry`

Build a unified list of calendar items from the article's `CalendarEntry`s
(maintenance, loans, and the occasion entries reached via the packlist) plus the
expiry date, each with a `type`, `start` and `end`. The grid and the list render
this list type-agnostically. Rationale: all terms already share the calendar
entry; the UI should not special-case each source.

### Decision 2: Server-side month grid

A helper computes the weeks and day cells for a month and places each item as a
bar (spanning its days, wrapped per week with lanes for overlaps) or a dot.
Rationale: no calendar JS library, deterministic output, testable.

### Decision 3: Lazy loading with HTMX `revealed` sentinels

The scroll area holds month blocks; a sentinel above and below each end loads the
previous/next month (`hx-get` with `hx-trigger="revealed"`,
`hx-swap="afterbegin"/"afterend"`). When prepending, the scroll position is
compensated by the added height so the view does not jump. Rationale: reuses the
existing HTMX stack; no polling.

### Decision 4: Selection client-side, conflict check server-side

JS tracks the pending selection (start, end) in the grid (first tap, same-day,
other-day, × / outside to cancel). On confirmation an HTMX request returns either
the conflict popup (the overlapping terms) or the action chooser. Rationale: the
overlap query belongs on the server; the interaction stays snappy.

### Decision 5: Generic entry edit/delete

New endpoints edit and delete a `CalendarEntry` (title, start, end). This covers
maintenance, loans and occasions uniformly. An occasion term additionally links
to its detail page; the expiry date is edited as the article's field. Rationale:
one code path instead of per-type endpoints.

### Decision 6: Popups as overlays

The preview, conflict list, action choice and entry form use a full-screen
overlay (like the image lightbox) so they work above the detail modal. Rationale:
avoids nested Bootstrap modals.

### Decision 7: Per-user switch setting

Add `detail_calendar_view` (`calendar` default, `list`) to the user profile and
resolve it like `detail_layout_desktop`; the switch is a URL override plus the
setting. Rationale: same mental model as the existing detail layout setting.

## Risks / Trade-offs

- **Bars across weeks/months need lane assignment** → compute lanes server-side
  and keep the algorithm small; a bar only needs to know its start/end columns
  per week row.
- **Upward lazy-load can jump the scroll** → compensate by the height of the
  prepended block.
- **New endpoints for entry edit/delete** → cover them with tests; deleting an
  entry cascades to its occasion/loan (1:1).
- **Many months in the DOM** → load only on demand, one month per sentinel.

## Migration Plan

A profile field with a default; no data migration. Rollback reverts the
templates/views; the setting can stay.

## Open Questions

- Whether a loan's party/status should be editable from the term popup (for now
  it links to the loan page).
- The exact number of months loaded per scroll step (start with one).
