## Context

§8 describes an onboarding wizard. The configuration page exists; this change
adds the guided first-run flow.

## Goals / Non-Goals

**Goals:**

- A wizard page with the questions and the suggested defaults.
- A completion flag and a restart link.

**Non-Goals:**

- Real multi-step navigation (one page is enough).
- A `setup_defaults` management command with profiles; `ONBOARDING_SKIP`.

## Decisions

### Decision 1: One page, not five steps

The questions and the suggestions live on one page; the answers pre-select the
suggestions. This covers the flow without multi-step state.

### Decision 2: Reuse the standard types

The suggestions are the §8 standard article/storage types (already used by the
configuration page) and `ensure_role_templates`.

### Decision 3: A completion flag

`hub.Settings.onboarding_completed`; the configuration page links to restart.

## Risks / Trade-offs

- [No auto-redirect on first start] → the wizard is reachable from the hub/config;
  auto-redirect is a later refinement.

## Migration Plan

- One field on `hub.Settings`.
