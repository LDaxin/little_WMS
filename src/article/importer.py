"""CSV import of articles (§19).

Two steps: ``preview_import`` classifies the rows without creating anything,
then ``import_articles`` applies the user's choices. The delimiter and the
header names (German or English) are detected, so a German Excel export works.
"""
import csv
import io
from decimal import Decimal, InvalidOperation

from article.models import Article, ArticleBase, ArticleType, Stock, ZUSTAND_CHOICES
from storage.models import Storage, StorageType

# Header aliases (lowercased) -> canonical column.
HEADER_ALIASES = {
    "name": "name",
    "typ": "type",
    "type": "type",
    "menge": "menge",
    "quantity": "menge",
    "anzahl": "menge",
    "lagerort": "storage",
    "lager": "storage",
    "storage": "storage",
    "ort": "storage",
    "zustand": "zustand",
    "condition": "zustand",
}


def parse_csv(text):
    """Parse CSV text into a list of ``(row_number, canonical_row)`` pairs."""
    reader = csv.reader(io.StringIO(text), delimiter=_detect_delimiter(text))
    rows = list(reader)
    if not rows:
        return []
    header = [_canonical(cell) for cell in rows[0]]
    parsed = []
    for row_number, raw in enumerate(rows[1:], start=2):
        if not any(cell.strip() for cell in raw):
            continue
        row = {}
        for key, value in zip(header, raw):
            if key:
                row[key] = value
        parsed.append((row_number, row))
    return parsed


def _detect_delimiter(text):
    first_line = text.splitlines()[0] if text.splitlines() else ""
    if first_line.count(";") > first_line.count(","):
        return ";"
    if first_line.count("\t") > first_line.count(","):
        return "\t"
    return ","


def _canonical(header):
    return HEADER_ALIASES.get(header.strip().lower(), "")


def _row_error(row):
    """Validate the fields that do not depend on the database."""
    name = (row.get("name") or "").strip()
    if not name:
        return "missing name"
    if len(name) > 20:
        return "name too long (max 20)"
    if not (row.get("type") or "").strip():
        return "missing type"
    menge_raw = (row.get("menge") or "").strip() or "1"
    try:
        Decimal(menge_raw)
    except InvalidOperation:
        return "invalid menge: %s" % menge_raw
    zustand = (row.get("zustand") or "").strip() or "gut"
    if zustand not in dict(ZUSTAND_CHOICES):
        return "invalid zustand: %s" % zustand
    return None


def preview_import(rows, organisation):
    """Classify rows without creating anything."""
    valid = []
    errors = []
    unknown_types = set()
    unknown_storages = set()
    duplicates = []
    for row_number, row in rows:
        error = _row_error(row)
        if error:
            errors.append((row_number, error))
            continue
        name = row["name"].strip()
        type_name = row["type"].strip().lower()
        article_type = ArticleType.objects.filter(organisation=organisation, name=type_name).first()
        if article_type is None:
            unknown_types.add(type_name)
        storage_name = (row.get("storage") or "").strip()
        if storage_name and not Storage.objects.filter(
            organisation=organisation, name=storage_name
        ).exists():
            unknown_storages.add(storage_name)
        if article_type is not None and ArticleBase.objects.filter(
            organisation=organisation, name=name, pType=article_type
        ).exists():
            duplicates.append((row_number, name, type_name))
        valid.append((row_number, row))
    return {
        "total": len(rows),
        "valid": valid,
        "errors": errors,
        "unknown_types": sorted(unknown_types),
        "unknown_storages": sorted(unknown_storages),
        "duplicates": duplicates,
    }


def import_articles(rows, organisation, type_choices=None, storage_choices=None, duplicates="skip"):
    """Import rows, applying the preview choices. Returns a report dict."""
    type_choices = type_choices or {}
    storage_choices = storage_choices or {}
    imported = updated = skipped = 0
    errors = []
    for row_number, row in rows:
        error = _row_error(row)
        if error:
            errors.append((row_number, error))
            continue

        name = row["name"].strip()
        type_name = row["type"].strip().lower()
        article_type = _resolve_type(organisation, type_name, type_choices.get(type_name))
        if article_type is None:
            errors.append((row_number, "unknown type: %s" % type_name))
            continue

        stored = None
        storage_name = (row.get("storage") or "").strip()
        if storage_name:
            storage = _resolve_storage(organisation, storage_name, storage_choices.get(storage_name))
            if storage is None:
                errors.append((row_number, "unknown storage: %s" % storage_name))
                continue
            stored = storage.space

        menge = Decimal((row.get("menge") or "").strip() or "1")
        zustand = (row.get("zustand") or "").strip() or "gut"

        base = ArticleBase.objects.filter(
            organisation=organisation, name=name, pType=article_type
        ).first()
        if base is not None:
            if duplicates == "skip":
                skipped += 1
                continue
            article = Article.objects.filter(organisation=organisation, base=base).first()
            if article is None:
                article = Article.objects.create(organisation=organisation, base=base)
            article.zustand = zustand
            article.save()
            _set_stock(article, stored, menge)
            updated += 1
            continue

        base = ArticleBase.objects.create(organisation=organisation, name=name, pType=article_type)
        article = Article.objects.create(organisation=organisation, base=base, zustand=zustand)
        _set_stock(article, stored, menge)
        imported += 1
    return {"imported": imported, "updated": updated, "skipped": skipped, "errors": errors}


def _resolve_type(organisation, type_name, choice):
    article_type = ArticleType.objects.filter(organisation=organisation, name=type_name).first()
    if article_type is not None:
        return article_type
    if choice == "create":
        return ArticleType.objects.create(
            organisation=organisation, name=type_name, symbol=type_name[:2].upper()
        )
    if choice and choice.isdigit():
        return ArticleType.objects.filter(organisation=organisation, pk=int(choice)).first()
    return None


def _resolve_storage(organisation, storage_name, choice):
    storage = Storage.objects.filter(organisation=organisation, name=storage_name).first()
    if storage is not None:
        return storage
    if choice == "create":
        storage_type, _ = StorageType.objects.get_or_create(
            organisation=organisation, name="other", defaults={"symbol": "SO"}
        )
        return Storage.objects.create(organisation=organisation, name=storage_name, typ=storage_type)
    if choice and choice.isdigit():
        return Storage.objects.filter(organisation=organisation, pk=int(choice)).first()
    return None


def _set_stock(article, stored, menge):
    stock, _ = Stock.objects.get_or_create(article=article, stored=stored, defaults={"menge": menge})
    stock.menge = menge
    stock.save()
