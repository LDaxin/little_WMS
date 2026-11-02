"""Search helpers."""
from django.db.models import Q


def filter_by_search(queryset, search, *fields):
    """Filter ``queryset`` by ``search`` over ``fields`` (OR, ``contains``).

    An empty search returns the queryset unchanged.
    """
    if not search:
        return queryset
    q = Q()
    for field in fields:
        q |= Q(**{"%s__contains" % field: search})
    return queryset.filter(q)
