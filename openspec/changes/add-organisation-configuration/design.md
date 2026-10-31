## Context

§8 describes standard configurations and onboarding. The organisation admin
needs to create article types, storage types, and role templates; only role
templates exist so far.

## Goals / Non-Goals

**Goals:**

- A configuration page to manage article types and storage types.
- Load the §8 standard types.
- Create the standard role templates.

**Non-Goals:**

- The multi-step onboarding wizard.
- A custom-fields editor for article types.
- A `setup_defaults` management command.

## Decisions

### Decision 1: A configuration page, not a wizard

A single page with two lists (article types, storage types) plus "load defaults"
and "create role templates" covers the need without the wizard's question flow.

### Decision 2: Standard types from §8

The defaults are the §8 tables: article types Tent, Kitchen, Tool, Office,
Sport, Tech, Box/Crate, Consumable, Other; storage types Building, Room, Shelf,
Compartment, Cabinet, Container, Vehicle.

### Decision 3: Role templates reuse `ensure_role_templates`

The existing `organisation.permissions.ensure_role_templates` creates the
standard templates.

### Decision 4: Permission

The configuration page requires `settings.edit_all`.

## Risks / Trade-offs

- [No custom fields yet] → article types are created with name/symbol/toggle;
  custom fields are a later change.

## Migration Plan

- None.
