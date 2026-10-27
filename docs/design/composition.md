# Composition — Sets, Default Locations and Consumables

> Design note. Replaces the `ArticleSetItem` approach of step 2.3 and the
> per-article `standard_lagerplatz`.
> Reference: Lastenheft §4d (Sets/Bundles), §5b (QR Workflow), §11 (Movement).

## Concept

A storage location (`Space`) declares **what should be in it**: a *composition*
of `(ArticleBase, target quantity, minimum quantity)`. This is the single source
of truth for "what belongs where".

Two things fall out of this:

- **Sets** need no separate model. A container already holds its parts
  (`Article.objects.filter(stored=container.space)`), and moving the container
  moves its contents implicitly. A "set" is simply a location with a composition.
- **`standard_lagerplatz` is removed.** The default location of an article is
  *derived* from the compositions that mention its base — the relationship is
  built from the location side, not the article side.

## Data model

```python
class CompositionItem(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="composition")
    base = models.ForeignKey(ArticleBase, on_delete=models.CASCADE, related_name="composition_items")
    soll_menge = models.IntegerField(null=True, blank=True)      # blank = "any amount"
    mindestmenge = models.IntegerField(null=True, blank=True)    # blank = no minimum

    class Meta:
        unique_together = ("space", "base")
```

- `soll_menge` **blank** → no target, no check, no suggestion ("any amount",
  e.g. ironing beads).
- `mindestmenge` **blank** → no minimum, never a refill hint.

Lives in the `article` app (it references `ArticleBase`); the `space` app stays
free of `article` imports.

## Actual vs target

- **Ist** = sum of `menge` (or 1) of articles with `stored == space` and
  `base == base`.
- **Soll** = `soll_menge`, **Min** = `mindestmenge`.

| Condition | Behaviour |
|---|---|
| `soll_menge` blank | no check at all |
| Ist < Soll | location is **underfilled** → suggested as a target |
| Ist >= Soll | **"already enough"** → info + decision when storing anyway |
| Ist < Min | **"should be refilled"** hint |

## Over-allocation

The targets of all locations are compared against the articles that exist:
`sum(soll_menge)` for a base vs the number of articles of that base. If more is
allocated than exists, not every location can be filled.

- **Editing (A):** setting a target that over-allocates shows a warning and asks
  for confirmation ("Add anyway").
- **Display (C):** an over-allocated row is marked ("over-allocated (N available)").

Removing a composition item asks for confirmation.

## Default location (replaces `standard_lagerplatz`)

`Article.standard_lagerplatz` is removed. The default location of an article is
derived: every location whose composition contains the article's base **and is
underfilled**. Several locations can be suggested; a full one is not.

§5b "Where should it go?" becomes this reverse lookup. Affected today:
`storeToDefault`, `storeActions` (default display), the `where` page.

## Quantity, merge and consume

- `allow_merge_split = False` → `menge` is always **1**, hidden in the form.
- `allow_merge_split = True` → `menge` editable.
- **`menge = 0` → the article is soft-deleted** (used up). One choke point, not
  per view.
- **Merge** A + B → A (sum), B soft-deleted.

## Sets

A "set" is a location with a composition. No separate set model, no service
expansion, no movement-buffer expansion.

## Impact

- New model `CompositionItem` + migration.
- Remove `Article.standard_lagerplatz` + migration.
- Rework §5b (where page, store-to-default, storeActions) to the reverse lookup.
- Rework step 2.3: drop `ArticleSetItem`, the service expansion and the buffer
  expansion; keep only the composition editor + check.
- Merge/consume service + the `menge = 0` rule.
- UI: composition editor on the location detail; suggestions + "already enough"
  info on store.

## Decisions

- **Ist with merged articles:** sum `menge` — one article with `menge = 12`
  counts as 12.
- **`menge = 0`:** ask for confirmation before the article is soft-deleted.
