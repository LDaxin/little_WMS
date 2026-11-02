## Why

§11 lists sound and haptic feedback as part of the movement redesign: a short
beep on a successful scan, a different tone on an error, and vibration on mobile.
The movement redesign is otherwise built (buffer, target, store/remove, undo,
session), but this part was deferred and never finished.

## What Changes

- Per-user feedback settings on `UserProfile`: `sound_enabled`,
  `vibration_enabled`, `volume`.
- A "Feedback" section in the preferences page to edit them.
- The scan view signals the outcome to the client via an `HX-Trigger` response
  header (`movementScan` on success, `movementError` on error).
- The movement page plays a short beep (Web Audio API) and vibrates
  (`navigator.vibrate`) on those events, honouring the user's settings.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `movement`: scanning gives audible and haptic feedback, configurable per user.

## Impact

- `organisation` app: `UserProfile` fields + migration.
- `hub` app: preferences view and template.
- `movement` app: scan view response header, movement template script.
