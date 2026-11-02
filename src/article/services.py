"""Composition logic (§4d, docs/design/composition.md).

A storage location declares what should be in it; these helpers compare the
declared target against what is actually stored there.
"""
from django.db.models import Sum


def actual_quantity(space, base):
    """Sum of ``Stock.menge`` of ``base`` stored in ``space``."""
    from article.models import Stock

    total = Stock.objects.filter(stored=space, article__base=base).aggregate(
        total=Sum("menge")
    )["total"]
    return total or 0


def composition_status(space):
    """Per composition item: actual quantity and state flags.

    ``underfilled`` – below the target (``soll_menge``), so the location is a
    candidate for storing more. ``refill`` – below the minimum
    (``mindestmenge``). ``over`` – the base is over-allocated across all
    locations (more target than articles exist). All are False when the
    respective value is blank. ``global`` is the base's global minimum,
    ``min_sum`` the sum of all its per-location minimums.
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
            "global": item.base.mindestbestand,
            "min_sum": location_minimum_sum(item.base),
            "available": alloc["available"],
            "over": alloc["over"],
            "underfilled": item.soll_menge is not None and ist < item.soll_menge,
            "refill": item.mindestmenge is not None and ist < item.mindestmenge,
        })
    return status


def location_minimum_sum(base):
    """Sum of the per-location minimums declared for ``base`` (§4d)."""
    from article.models import CompositionItem

    return sum(item.mindestmenge or 0 for item in CompositionItem.objects.filter(base=base))


def allocation(base):
    """Total target across all locations vs available articles of ``base``.

    ``over`` is True when more is allocated (sum of ``soll_menge``) than there
    are articles of that base — then not every location can be filled.
    """
    from article.models import Article, CompositionItem

    total_soll = sum(item.soll_menge or 0 for item in CompositionItem.objects.filter(base=base))
    available = Article.objects.filter(base=base).count()
    return {"soll": total_soll, "available": available, "over": total_soll > available}


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
