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
    def store_article(article, target_space, user=None, amount=None, session=None):
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
            log("moved", article, user,
                {"to": str(target_space), "to_id": target_space.pk, "amount": float(qty)},
                session=session)
        else:
            stock = article.stocks.first()
            if stock is None:
                Stock.objects.create(article=article, stored=target_space, menge=1)
            else:
                stock.stored = target_space
                stock.menge = 1
                stock.save()
            log("moved", article, user,
                {"to": str(target_space), "to_id": target_space.pk}, session=session)
        return article

    @staticmethod
    @transaction.atomic
    def store_articles(articles, target_space, user=None, session=None):
        """Store several articles at once; all or nothing."""
        for article in articles:
            MovementService.store_article(article, target_space, user, session=session)
        return articles

    @staticmethod
    def remove_article(article, space=None, user=None, session=None):
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
        changes = {"from": str(stock.stored), "from_id": stock.stored_id, "amount": float(stock.menge)}
        stock.delete()
        log("removed", article, user, changes, session=session)
        return article


def undo(entry, user=None):
    """Reverse a logged movement and mark the original entry undone (§11).

    ``moved`` is undone by removing the article from its target space,
    ``removed`` by storing it back to where it came from. The counter-entry is
    itself logged (and can be undone again = redo).
    """
    from space.models import Space

    if entry.undone:
        raise ValidationError("Already undone")
    article = entry.content_object
    if entry.action == "moved":
        space = Space.objects.filter(pk=entry.changes.get("to_id")).first()
        MovementService.remove_article(article, space=space, user=user, session=entry.session)
        counter = log("removed", article, user,
                      {"from_id": entry.changes.get("to_id"), "undo_of": entry.pk},
                      session=entry.session)
    elif entry.action == "removed":
        space = Space.objects.filter(pk=entry.changes.get("from_id")).first()
        MovementService.store_article(article, space, user, session=entry.session)
        counter = log("moved", article, user,
                      {"to_id": entry.changes.get("from_id"), "undo_of": entry.pk},
                      session=entry.session)
    else:
        raise ValidationError("Cannot undo %s" % entry.action)
    entry.undone = True
    entry.save()
    return counter

