"""Storage integrity rules (§21).

Space-focused: works only with `Space` objects, so the `space` app does not
have to import `article`/`storage` (which depend on it).
"""


def max_storage_depth():
    """Configured maximum storage depth (`hub.Settings.storageDepth`)."""
    from hub.models import Settings

    settings = Settings.objects.first()
    return settings.storageDepth if settings else 7


def can_store(owner_space, target_space, max_depth):
    """Check whether an object may be stored in `target_space`.

    `owner_space` is the `Space` of the object being stored (or `None` if it has
    none). Returns `(True, "")` or `(False, "reason")`.
    """
    if owner_space is not None and owner_space.pk == target_space.pk:
        return False, "Cannot be stored in itself"
    space, depth = target_space, 0
    while space is not None:
        depth += 1
        if depth > max_depth:
            return False, "Maximum storage depth (%s) exceeded" % max_depth
        if owner_space is not None and space.pk == owner_space.pk:
            return False, "Cycle detected"
        space = parent_space(space)
    return True, ""


def parent_space(space):
    """The Space that contains `space` (via its owning container article), or None."""
    owner = getattr(space, "itemArticle", None)
    if owner is None:
        return None
    stock = owner.stocks.exclude(stored=None).first()
    return stock.stored if stock else None


def storage_chain(storage):
    """Names from the top-level storage down to `storage`."""
    parts = []
    while storage is not None:
        parts.append(storage.name)
        storage = storage.parent
    return list(reversed(parts))


def space_path(space):
    """Human-readable breadcrumb for a Space, e.g. "Building A > Room 2 > Shelf 3"."""
    articles = []
    while space is not None:
        owner = getattr(space, "itemArticle", None) or getattr(space, "itemStorage", None)
        if owner is None:
            break
        if hasattr(owner, "parent"):  # Storage
            return " > ".join(storage_chain(owner) + list(reversed(articles)))
        articles.append(owner.base.name)
        stock = owner.stocks.exclude(stored=None).first()
        space = stock.stored if stock else None
    return " > ".join(reversed(articles))
