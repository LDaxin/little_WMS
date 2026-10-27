# Stock — separating identity from quantity

> Design note. Reworks the `Article` model so that merge/split become natural
> quantity operations instead of ad-hoc edits on an identity.
> Reference: Lastenheft §4d (Sets/Bundles), §11 (Movement), §5b (QR Workflow).

## Concept

An `Article` is the **identity** of a thing (code, type, attributes, condition,
history). A `Stock` is a **quantity of that Article at a location** — it has no
identity of its own. Merge and split are then plain quantity operations on
`Stock`; no identity is ever created or destroyed.

This keeps the movement/composition logic simple: they still work with "things
at a location", only that thing is now called `Stock`.

## Model

- **`ArticleType`** (category) — unchanged (`article_toggle_space`,
  `allow_merge_split`, `field_config`, `custom_fields_schema`).
- **`ArticleBase`** (catalog item) — unchanged.
- **`Article`** (identity) — `base`, `code`, `space` (container), `attributes`,
  `tags`, global fields (`zustand`, `kaufdatum`, …). **Loses `stored` and
  `menge`.**
- **`Stock`** (quantity at a location):

```python
class Stock(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="stocks")
    stored = models.ForeignKey(Space, on_delete=models.SET_NULL, null=True, blank=True)
    menge = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    class Meta:
        unique_together = ("article", "stored")
```

- An `Article` has **several** `Stock` lines (one per location).
- QR codes stay on the `Article`; the `Stock` has no code.
- Condition/attributes stay on the `Article`.

## Movement

- **Store** an article into a target: find-or-create the `Stock` for
  `(article, target)` and increase `menge`. (This *is* the merge.)
- **Remove**: decrease the `Stock`'s `menge`; at 0 the `Stock` line is deleted.
  (This *is* the split.)
- **Partial store/remove**: just a quantity change — no new article, no new code.
- `allow_merge_split = False` → an article has at most one `Stock` with
  `menge = 1` (a unique object).

## Composition

- Still references `ArticleBase`. The check counts the `Stock` quantities of that
  base at the location: `sum(stock.menge for stock in Stock.objects.filter(stored=space, article__base=base))`.

## Sets / containers

- A container is an `Article` with a `space`. Its contents are the `Stock` lines
  with `stored == container.space`.

## Migration

The database runs on `dev`, so the migration history is **not reset**. Instead all
migrations added since `dev` are **squashed**: one fresh migration per app,
generated from the `dev` migration state; `dev`'s migrations stay. A data
migration then moves `Article.stored`/`menge` into `Stock`.

## Decisions

- `Article.amount` (legacy `CharField`) — **removed**.
- `mindestbestand` — **global on `ArticleBase`** (a property of the kind), plus
  **per location** via the composition (`mindestmenge`). The two hint each other;
  a button sets the global minimum to the sum of the location minima.
- The movement buffer holds `Article`s (identity); the store resolves the `Stock`.
- "Not stored" — a `Stock` with `stored = None` (not "no row"), and it triggers
  the hints.
