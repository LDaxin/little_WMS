"""CSV import of articles (§19).

Fixed columns: ``name``, ``type``, ``menge``, ``storage``, ``zustand``. Each row
is validated before anything is created, so a bad row never leaves a
half-created article.
"""
import csv
from decimal import Decimal, InvalidOperation

from article.models import Article, ArticleBase, ArticleType, Stock, ZUSTAND_CHOICES
from storage.models import Storage


def import_articles(file, organisation):
    """Import articles from a CSV file-like object. Returns a report dict."""
    reader = csv.DictReader(file)
    imported = 0
    errors = []
    for row_number, row in enumerate(reader, start=2):
        error = _import_row(row, organisation)
        if error:
            errors.append((row_number, error))
        else:
            imported += 1
    return {"imported": imported, "errors": errors}


def _import_row(row, organisation):
    """Validate and create one row. Returns an error string or None."""
    name = (row.get("name") or "").strip()
    if not name:
        return "missing name"
    if len(name) > 20:
        return "name too long (max 20)"

    type_name = (row.get("type") or "").strip().lower()
    if not type_name:
        return "missing type"
    article_type = ArticleType.objects.filter(organisation=organisation, name=type_name).first()
    if article_type is None:
        return "unknown type: %s" % type_name

    menge_raw = (row.get("menge") or "").strip() or "1"
    try:
        menge = Decimal(menge_raw)
    except InvalidOperation:
        return "invalid menge: %s" % menge_raw

    zustand = (row.get("zustand") or "").strip() or "gut"
    if zustand not in dict(ZUSTAND_CHOICES):
        return "invalid zustand: %s" % zustand

    stored = None
    storage_name = (row.get("storage") or "").strip()
    if storage_name:
        storage = Storage.objects.filter(organisation=organisation, name=storage_name).first()
        if storage is None:
            return "unknown storage: %s" % storage_name
        stored = storage.space

    base, _ = ArticleBase.objects.get_or_create(
        organisation=organisation, name=name, pType=article_type
    )
    article = Article.objects.create(organisation=organisation, base=base, zustand=zustand)
    Stock.objects.create(article=article, stored=stored, menge=menge)
    return None
