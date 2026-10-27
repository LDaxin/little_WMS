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
    (``mindestmenge``). ``over`` – the base is over-allocated across all
    locations (more target than articles exist). All are False when the
    respective value is blank.
    """
    status = []
    for item in space.composition.select_related("base"):
        ist = actual_quantity(space, item.base)
        alloc = allocation(item.base)
        status.append({
            "item": item,
            "ist": ist,
            "soll": item.soll_menge,
            "min": item.mindestmenge,
            "available": alloc["available"],
            "over": alloc["over"],
            "underfilled": item.soll_menge is not None and ist < item.soll_menge,
            "refill": item.mindestmenge is not None and ist < item.mindestmenge,
        })
    return status


def allocation(base):
    """Total target across all locations vs available articles of ``base``.

    ``over`` is True when more is allocated (sum of ``soll_menge``) than there
    are articles of that base — then not every location can be filled.
    """
    from article.models import Article, CompositionItem

    total_soll = sum(item.soll_menge or 0 for item in CompositionItem.objects.filter(base=base))
    available = Article.objects.filter(base=base).count()
    return {"soll": total_soll, "available": available, "over": total_soll > available}


def consume(article, amount=1):
    """Reduce an article's quantity; soft-delete it when it reaches 0 (§4d).

    The single choke point for consuming a consumable.
    """
    article.menge = (article.menge or 1) - amount
    if article.menge <= 0:
        article.delete()
    else:
        article.save()
    return article


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
