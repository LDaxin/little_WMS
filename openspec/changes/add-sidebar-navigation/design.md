## Context

§12 lists mobile & navigation. The app uses a top navbar. This change replaces
it with a vertical sidebar that adapts to mobile and desktop.

## Goals / Non-Goals

**Goals:**

- A vertical sidebar with logo, quick navigation, and the existing actions.
- Responsive: narrow rail, hover-expand (desktop), toggle (mobile).
- Per-user position (left/right) and view mode (auto/mobile/desktop).

**Non-Goals:**

- Auto-tracked most-used quick navigation.
- Per-view context actions (the existing bottom buttons stay).

## Decisions

### Decision 1: A CSS-only responsive sidebar

The sidebar is a fixed vertical rail; CSS media queries and `:hover` handle the
layout, so there is no separate mobile template. A small toggle button covers
touch devices where hover is unavailable.

### Decision 2: Per-user settings on the profile

`UserProfile.sidebar_position` and `UserProfile.view_mode` store the choice;
the header reads them. The view mode adds a CSS class (`view-mobile` /
`view-desktop`) that forces the layout regardless of the viewport.

### Decision 3: Quick navigation is fixed for now

Dashboard, articles, storages, and movement. Auto-tracking the most-used views
is deferred.

### Decision 4: Text size scales the root font

The text size is applied as the root (`html`) `font-size`; Bootstrap sizes
everything in `rem`, so the whole app (content and sidebar) scales. Icon size is
a separate CSS variable on the sidebar. Both are stored per desktop/mobile.

## Risks / Trade-offs

- [Hover-expand on touch] → a toggle button is provided.
- [Content padding] → the content area is offset by the rail width.

## Migration Plan

- New `UserProfile` columns with defaults; no data migration.
