## Context

`seed_demo` builds a small realistic dataset for development. It predates the
occasion system and does not cover it.

## Goals / Non-Goals

**Goals:**

- Seed locations, occasion types, occasions (+ packlist), and occasion templates.
- Stay idempotent.

**Non-Goals:**

- Seeding recurrence rules (optional; can be added later).
- A user-facing capability (this is a developer tool).

## Decisions

### Decision 1: Extend the existing command

Add `_locations`, `_occasion_types`, `_occasions`, and `_occasion_templates`
methods to `seed_demo`, following the existing `get_or_create` pattern.

### Decision 2: No spec delta

The seed is a developer tool, not user-facing behaviour, so the change carries
no spec delta and is archived with `--skip-specs`.

## Risks / Trade-offs

- [Idempotency] → use `get_or_create` everywhere, keyed on stable names.

## Migration Plan

- None.
