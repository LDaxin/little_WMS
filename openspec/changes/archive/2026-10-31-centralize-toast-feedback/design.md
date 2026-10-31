## Context

Toast feedback is duplicated across five view modules. This is a pure refactor.

## Goals / Non-Goals

**Goals:**

- One helper to render a toast.
- Remove the repeated context dicts.

**Non-Goals:**

- Changing the toast markup or behaviour.
- A spec delta (behaviour unchanged).

## Decisions

### Decision 1: A helper in `hub/toasts.py`

`toast(request, name, text, type="status", template=...)` renders the toast
module and derives `toastId` from the type (`errorToast` for `alert`, else
`successToast`). `success_toast`/`error_toast` are thin shortcuts.

### Decision 2: Keep the template

The `hub/modules/toast.html` module is unchanged; the helper only builds its
context.

## Risks / Trade-offs

- [Toast id derived from type] → the id is only a jQuery selector; the toast has
  no type-specific styling, so this is cosmetic.

## Migration Plan

- None.
