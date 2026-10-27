"""Store/remove business logic (§7a, §11).

Used by the article/storage views now; the movement view follows in §2.1.
"""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from audit.services import log
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
    """Storing and removing articles – shared by views and (later) the API.

    Quantity lives on ``Stock`` (article, location); store/remove move it between
    the target location and the article's "not stored" line (``stored=None``).
    """

    @staticmethod
    def store_article(article, target_space, user=None, amount=None):
        """Store (part of) an article into ``target_space``.

        A merge/split article (§4d) moves ``amount`` (default: all) from its
        "not stored" line onto the target line, adding to any line already there.
        A non-mergeable article is a single object (``menge=1``) that is simply
        moved to the target.
        """
        from article.models import Stock

        if target_space is None:
            raise ValidationError("No target space")
        if not target_space.active:
            raise ValidationError("Target space is not active")
        ok, reason = can_store(article.space, target_space, max_storage_depth())
        if not ok:
            raise ValidationError(reason)

        if article.base.pType.allow_merge_split:
            source = article.stocks.filter(stored=None).first()
            qty = Decimal(amount) if amount is not None else (source.menge if source else Decimal(1))
            target, _ = Stock.objects.get_or_create(
                article=article, stored=target_space, defaults={"menge": 0}
            )
            target.menge += qty
            target.save()
            if source is not None:
                source.menge -= qty
                if source.menge <= 0:
                    source.delete()
                else:
                    source.save()
            log("moved", article, user, {"to": str(target_space), "amount": float(qty)})
        else:
            stock = article.stocks.first()
            if stock is None:
                Stock.objects.create(article=article, stored=target_space, menge=1)
            else:
                stock.stored = target_space
                stock.menge = 1
                stock.save()
            log("moved", article, user, {"to": str(target_space)})
        return article

    @staticmethod
    @transaction.atomic
    def store_articles(articles, target_space, user=None):
        """Store several articles at once; all or nothing."""
        for article in articles:
            MovementService.store_article(article, target_space, user)
        return articles

    @staticmethod
    def remove_article(article, space=None, user=None):
        """Remove an article's quantity back to its "not stored" line."""
        from article.models import Stock

        if space is None:
            stock = article.stocks.exclude(stored=None).first()
        else:
            stock = article.stocks.filter(stored=space).first()
        if stock is None:
            return article
        source, _ = Stock.objects.get_or_create(
            article=article, stored=None, defaults={"menge": 0}
        )
        source.menge += stock.menge
        source.save()
        changes = {"from": str(stock.stored), "amount": float(stock.menge)}
        stock.delete()
        log("removed", article, user, changes)
        return article

