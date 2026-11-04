## Context

A list page renders, above the list, a search bar (with the QR button), a
control bar (columns, table/cards toggle, select, select all) and — for
articles — an advanced-search trigger plus its panel. They are siblings of
`#list` inside `.content`, which on list pages is a flex column
(`body:has(#list) .content { display:flex; flex-direction:column; overflow:hidden }`)
with `#list` growing (`flex: 1 1 auto`) and `#listBody` scrolling. The QR
scanner panel is rendered in `#scannerDiv<field>` right after the search bar, so
its position follows the search bar.

## Goals / Non-Goals

**Goals:**

- Mobile: the search bar and the control bar sit below the list, pinned at the
  bottom, always visible — search bar bottom-most, control bar above it.
- The advanced-search trigger sits with the search field (next to the QR
  button) on mobile and desktop; its panel opens upward (mobile) / downward
  (desktop).
- The scanner panel always opens above the list.

**Non-Goals:**

- The floating action buttons (add / delete / export / QR) — separate follow-up.
- Advanced search on the storage list — later.
- The list rendering itself (table/cards), sorting, pagination, selection.

## Decisions

### Decision 1: Reorder in the flex flow, not a fixed overlay

Wrap the search bar and the control bar in a `#listControls` container and give
it `order` in the existing flex column so it follows `#list` in the mobile
layout. Because `#listControls` stays in the flow, the pinned controls never
cover the last rows — no extra bottom padding hack. The search bar and control
bar are ordered inside the wrapper so the search bar is bottom-most.
(Alternative: a `position: fixed` bottom bar — rejected: it overlaps content and
needs padding bookkeeping.)

### Decision 2: Reuse the existing mobile signal

The reorder applies under the existing mobile-layout signal used elsewhere in
the app: `body.view-mobile` (forced mobile) and the `@media (max-width: 768px)`
block (auto), scoped to `body:has(#list)`; `body.view-desktop` keeps the desktop
order. This matches the sidebar/view-mode handling instead of inventing a new
breakpoint.

### Decision 3: Advanced trigger joins the search field

Move the advanced trigger button into the search input-group next to the QR
button (mobile and desktop). The panel (`#queryBuilder`) becomes an absolutely
positioned panel anchored to the trigger instead of a block in the flow, so its
direction is controlled by CSS: `bottom: 100%` in the mobile layout,
`top: 100%` in the desktop layout. `qbToggle()` keeps toggling visibility.

### Decision 4: Scanner stays above the list

Move `#scannerDiv<field>` out of the search area to directly above `#list`, so
the scanner opens above the list regardless of where the search bar sits. The
QR button keeps targeting the same element id.

### Decision 5: Mobile controls follow the sidebar side

In the mobile layout, align the control bar and the search-field buttons (QR,
advanced) to the sidebar side. Derive the side from the existing per-device
sidebar position (`sidebar_position_mobile`) — exposed as a `sidebar-mobile-*`
class on `<body>` and selected via the existing `@media (max-width: 768px)` /
`body.view-mobile` / `body.view-desktop` pattern. A right sidebar right-aligns
the control bar (`justify-content: flex-end`); a left sidebar moves the search
buttons before the input (`order`) so they sit on the left, adjusting the input's
border radius. No new setting: the sidebar position already expresses the user's
handedness preference.

(Alternative: a separate "controls side" setting — rejected as YAGNI; it can be
added later if the two need to diverge.)

### Decision 6: Size the mobile list to the visual viewport

`height: 100vh` ignores the on-screen keyboard, so the browser pans the document
to reveal the bottom search field and the results scroll off the top. Set a
`--app-height` from `window.visualViewport.height` (VisualViewport API —
supported by Firefox Android, Chrome/Android and Safari) and use it for the list
layout height. Detect the keyboard as a drop of more than 150 px from the largest
viewport height seen (reset on rotation) and add a `keyboard-open` class that
collapses the control bar, so the results keep the room.

(Alternative: Chrome-only `VirtualKeyboard` API / `env(keyboard-inset-height)` —
rejected, not cross-browser.)

## Risks / Trade-offs

- [Advanced panel clipped by `overflow:hidden` on `.content`] → anchor the
  panel to a trigger inside `#listControls` (outside the scroll area) and give
  it a z-index; verify visually on both layouts.
- [`body:has(#list)` support] → already used by the current list CSS, so no new
  requirement.
- [Pinned controls reduce the list height] → expected; `#listBody` keeps
  scrolling, so no rows are hidden.
- [The scanner opening above the list shrinks the list while open] → accepted;
  it is the requested behaviour.

## Migration Plan

Template/CSS only — no data or schema changes. Deploy by rebuilding the image;
rollback by reverting the commit.
