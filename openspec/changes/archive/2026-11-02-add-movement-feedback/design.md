## Context

The movement page scans codes via HTMX: the scan form posts to `movementScan`,
which re-renders the buffer. The client cannot tell a valid scan from an error
from the HTTP status alone (both are 200), so the outcome must be signalled
explicitly. Per-user UI settings already live on `UserProfile` and are edited on
the preferences page (sidebar, icon/text size).

## Goals / Non-Goals

**Goals:**

- Audible feedback on a successful scan, a different tone on an error.
- Vibration on mobile for both outcomes.
- Per-user on/off switches and a volume setting.

**Non-Goals:**

- Sound/haptic on store/remove (only scanning, as specified in §11).
- The "smart default for containers on/off" setting (a separate §11 setting).
- Audio files or a new dependency.

## Decisions

### Decision 1: Signal the outcome with `HX-Trigger`

`movementScan` sets the `HX-Trigger` response header to `movementScan` on
success or `movementError` on error. HTMX dispatches the event on the triggering
element; the movement page listens on `document.body`. This keeps the outcome
out of the HTML and needs no extra request.

### Decision 2: Generate the beep with the Web Audio API

No audio file and no library: an `OscillatorNode` produces a short tone (higher
on success, lower on error), with the gain taken from the user's `volume`.
Vibration uses `navigator.vibrate` (a no-op where unsupported).

### Decision 3: Settings on `UserProfile`

`sound_enabled`, `vibration_enabled` (both default on) and `volume` (0–100,
default 50) follow the existing per-user settings pattern and are edited on the
preferences page.

## Risks / Trade-offs

- [Autoplay policy] → the first beep may be blocked until the page has had a user
  gesture; scanning is a gesture, so this is acceptable.
- [Vibration support] → `navigator.vibrate` is absent on desktop; guarded.

## Migration Plan

- Add three columns to `organisation_userprofile` with defaults. Rollback: drop
  them.
