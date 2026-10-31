## Why

§8's philosophy is "everything easily movable = Article, everything hard to move
= Storage". Yet the standard storage types include Container and Vehicle, which
are movable. They fit the article model (with `article_toggle_space`, so they can
hold other articles and act as a storage location).

## What Changes

- Move Container and Vehicle from the standard storage types to the standard
  article types (with `article_toggle_space = True`).
- Update the Lastenheft §8 tables accordingly.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `organisations`: the standard configuration defaults.

## Impact

- `organisation/views.py` (`DEFAULT_ARTICLE_TYPES` / `DEFAULT_STORAGE_TYPES`),
  used by the configuration page and the onboarding wizard.
- `docs/Lastenheft.md` §8.
