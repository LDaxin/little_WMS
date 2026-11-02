"""Resolve scanned codes to their objects (§11, §26).

Centralises the ``s0``/``a0`` prefix logic so it is not scattered across views.
"""


def resolve_code(code):
    """Return ``(kind, object)`` for a code.

    ``kind`` is ``"storage"``, ``"article"``, or ``None`` for an unknown prefix.
    ``object`` is ``None`` when the prefix is known but no object matches.
    """
    from article.models import Article
    from storage.models import Storage

    if code.startswith("s0"):
        return "storage", Storage.objects.filter(code__code=code).first()
    if code.startswith("a0"):
        return "article", Article.objects.filter(code__code=code).first()
    return None, None
