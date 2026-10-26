"""Store/remove business logic (§7a, §11).

Used by the article/storage views now; the movement view follows in §2.1.
"""
from django.core.exceptions import ValidationError
from django.db import transaction

from space.services import can_store, max_storage_depth


def resolve_space(code):
    """Resolve a scanned code to the Space it represents.

    ``s0`` -> Storage, ``a0`` -> container Article. Raises ValidationError for
    anything else (centralizes the prefix logic, §11).
    """
    from article.models import Article
    from storage.models import Storage

    if code.startswith("s0"):
        try:
            return Storage.objects.get(code__code=code).space
        except Storage.DoesNotExist:
            raise ValidationError("No storage with code %s" % code)
    if code.startswith("a0"):
        try:
            return Article.objects.get(code__code=code).space
        except Article.DoesNotExist:
            raise ValidationError("No article with code %s" % code)
    raise ValidationError("Unknown code %s" % code)


class MovementService:
    """Storing and removing articles – shared by views and (later) the API."""

    @staticmethod
    def store_article(article, target_space, user=None):
        """Store/move an article into ``target_space``."""
        if target_space is None:
            raise ValidationError("No target space")
        ok, reason = can_store(article.space, target_space, max_storage_depth())
        if not ok:
            raise ValidationError(reason)
        article.stored = target_space
        article.save()
        return article

    @staticmethod
    @transaction.atomic
    def store_articles(articles, target_space, user=None):
        """Store several articles at once; all or nothing."""
        for article in articles:
            MovementService.store_article(article, target_space, user)
        return articles

    @staticmethod
    def remove_article(article, user=None):
        """Remove an article from its storage."""
        article.stored = None
        article.save()
        return article
