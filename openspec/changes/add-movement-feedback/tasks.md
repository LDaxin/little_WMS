## 1. Settings

- [x] 1.1 `UserProfile`: `sound_enabled`, `vibration_enabled`, `volume`
- [x] 1.2 Migration
- [x] 1.3 Preferences page "Feedback" section + save in `emailPreferences`

## 2. Feedback

- [x] 2.1 `movementScan` sets `HX-Trigger` (`movementScan` / `movementError`)
- [x] 2.2 Movement page: beep + vibration on those events, honouring the settings

## 3. Tests

- [x] 3.1 Scan success/error sets the trigger header
- [x] 3.2 Preferences save the feedback settings

## 4. Verify

- [x] 4.1 Full suite green in Docker
- [x] 4.2 Rebuild + restart
