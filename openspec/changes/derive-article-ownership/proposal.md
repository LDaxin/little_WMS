## Why

RF-004: `Article.ownership` (`owned`/`borrowed`) is a second source of truth for
"there is a loan". It is written in four places (borrow, return, confirm, share
link) but never read for behaviour, so it can drift from the actual `Loan`. The
loan is the real record.

## What Changes

- Remove the `Article.ownership` field; derive it from the open loan instead.
- `Article.ownership` becomes a property: `borrowed` while an open (pending or
  active) loan with direction `in` exists, otherwise `owned`.
- Drop the four write sites and the form excludes.
- Keep the API shape: `ownership` stays a read-only field on the article
  serializer.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `loans`: an article's ownership is derived from its open loan, not stored.

## Impact

- `article` app: model field removed + migration, form excludes.
- `loans` app: write sites removed.
- `savedviews` app: write site removed.
- `api` app: read-only `ownership` field.
