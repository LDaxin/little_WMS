## Why

§36 describes concurrency: two users editing the same article simultaneously
would lose one change. Movements are last-write-wins (fine), but edits need
optimistic locking.

## What Changes

- A `version` field on `Article` and `ArticleBase`.
- The article update form carries the loaded version; on save the version is
  compared and incremented, and a mismatch shows a conflict message.

## Capabilities

### New Capabilities

- `concurrency`: optimistic locking for edits.

### Modified Capabilities

<!-- none -->

## Impact

- `article` models gain `version`; the update view and form handle it.
- **Deferred**: a version on every model; automatic merging.
