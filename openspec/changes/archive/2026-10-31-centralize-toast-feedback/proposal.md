## Why

Toast feedback is built ad hoc in every view: a `context` dict with
`toastName`/`toastId`/`toastText`/`toastType` plus a `render(...)` call, repeated
~40 times across five view modules. The text and the id are easy to get wrong
(one block even used bare `toastName:` names, a latent `NameError`).

## What Changes

- A `hub/toasts.py` helper (`toast`, `success_toast`, `error_toast`) that renders
  the toast module and derives the id from the type.
- The five view modules use the helper instead of building the dict themselves.

## Capabilities

<!-- none: pure refactor, no behaviour change -->

## Impact

- `hub/toasts.py` (new); `article`, `storage`, `location`, `tag`, `codeSystem`
  views refactored.
- No spec delta (behaviour unchanged); archived with `--skip-specs`.
