"""Tag helpers (§13).

Tag inheritance is **computed**, not stored: an object inherits the tags of the
containers it currently sits in, but only for categories with
`inherit_to_contents=True`. Taking the object out of a container therefore
removes the inherited tags automatically.
"""


def effective_tags(obj):
    """Own tags plus tags inherited from the containers `obj` sits in."""
    from space.services import parent_space

    tags = set(obj.tags.all())
    stock = obj.stocks.exclude(stored=None).first() if hasattr(obj, "stocks") else None
    space = stock.stored if stock else None
    while space is not None:
        owner = getattr(space, "itemArticle", None) or getattr(space, "itemStorage", None)
        if owner is not None:
            for tag in owner.tags.all():
                if tag.category is not None and tag.category.inherit_to_contents:
                    tags.add(tag)
        space = parent_space(space)
    return tags
