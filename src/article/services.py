"""Composition logic (§4d, docs/design/composition.md).

A storage location declares what should be in it; these helpers compare the
declared target against what is actually stored there.
"""


def actual_quantity(space, base):
    """Sum of ``menge`` (or 1) of articles of ``base`` stored in ``space``."""
    from article.models import Article

    return sum((article.menge or 1) for article in Article.objects.filter(stored=space, base=base))


def composition_status(space):
    """Per composition item: actual quantity and state flags.

    ``underfilled`` – below the target (``soll_menge``), so the location is a
    candidate for storing more. ``refill`` – below the minimum
    (``mindestmenge``). Both are False when the respective value is blank.
    """
    status = []
    for item in space.composition.select_related("base"):
        ist = actual_quantity(space, item.base)
        status.append({
            "item": item,
            "ist": ist,
            "soll": item.soll_menge,
            "min": item.mindestmenge,
            "underfilled": item.soll_menge is not None and ist < item.soll_menge,
            "refill": item.mindestmenge is not None and ist < item.mindestmenge,
        })
    return status


def default_locations(base):
    """Locations whose composition mentions ``base`` and are underfilled.

    Replaces ``Article.standard_lagerplatz``: the default location is derived
    from the composition. A location with a blank ``soll_menge`` ("any amount")
    is never suggested.
    """
    from article.models import CompositionItem

    result = []
    for item in CompositionItem.objects.filter(base=base).select_related("space"):
        if item.soll_menge is None:
            continue
        if actual_quantity(item.space, base) < item.soll_menge:
            result.append(item.space)
    return result
