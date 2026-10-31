## Why

§2 describes copying occasions: "next year's camp = this year's dates + 364
days". Today an occasion can be saved as a template, but there is no way to
duplicate an existing occasion with its packlist.

## What Changes

- A "Duplicate" action on the occasion detail creates a copy with the same type,
  location, participant count, and packlist.
- The dates can be shifted by N days (default 0).

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `occasions`: duplicate an occasion.

## Impact

- New view/url in the `occasion` app; a "Duplicate" form on the occasion detail.
- **Deferred**: an empty date (the start date is required; the user edits the
  copy afterwards); copying a whole recurrence series.
