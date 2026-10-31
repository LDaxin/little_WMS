## Why

`seed_demo` is the way to get a usable dev dataset after a database reset, but it
only creates article types, storages, tags, and articles. Locations, occasion
types, occasions (+ packlist), and occasion templates are missing, so a reset
loses the occasion test data.

## What Changes

- Extend `seed_demo` to also create locations, occasion types, occasions with a
  packlist, and occasion templates.
- Keep it idempotent (safe to run repeatedly).

## Capabilities

<!-- none: this is a developer tool, not user-facing behaviour -->

## Impact

- `hub/management/commands/seed_demo.py` only.
- No model or migration change.
