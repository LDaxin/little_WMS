"""Query Builder parser (§9).

Translates the client's JSON query (AND/OR/NOT, nested groups) into Django ``Q``
objects. Only whitelisted fields and operators are allowed.
"""
import json

from django.db.models import Q


class QueryError(Exception):
    pass


# field -> type, per model
ARTICLE_FIELDS = {
    "base__name": "text",
    "code__code": "text",
    "zustand": "choice",
    "ist_verbrauchsartikel": "boolean",
    "gewicht_gramm": "number",
    "ablaufdatum": "date",
    "kaufdatum": "date",
    "tags__name": "text",
    "base__pType__name": "text",
}

# operator -> lookup suffix, per field type
OPERATORS = {
    "text": {
        "eq": "exact", "ne": "exact", "contains": "icontains",
        "starts": "istartswith", "ends": "iendswith",
        "empty": "isnull", "not_empty": "isnull",
    },
    "number": {
        "eq": "exact", "ne": "exact", "lt": "lt", "gt": "gt",
        "lte": "lte", "gte": "gte", "empty": "isnull",
    },
    "date": {
        "eq": "exact", "ne": "exact", "before": "lt", "after": "gt", "empty": "isnull",
    },
    "choice": {"eq": "exact", "ne": "exact"},
    "boolean": {"is_true": "exact", "is_false": "exact"},
}

NEGATED = {"ne", "empty", "is_false"}


def _condition(field, op, value, fields):
    if field not in fields:
        raise QueryError("unknown field: %s" % field)
    field_type = fields[field]
    if op not in OPERATORS[field_type]:
        raise QueryError("operator %s not allowed for %s" % (op, field))
    lookup = OPERATORS[field_type][op]
    if op in ("empty", "not_empty"):
        value = True
    elif op == "is_true":
        value = True
    elif op == "is_false":
        value = False
    q = Q(**{"%s__%s" % (field, lookup): value})
    if op in NEGATED:
        q = ~q
    return q


def parse(node, fields):
    """Translate a query node into a ``Q`` object."""
    if "conditions" in node:
        op = (node.get("type") or "AND").upper()
        q = None
        for child in node["conditions"]:
            child_q = parse(child, fields)
            if q is None:
                q = child_q
            elif op == "OR":
                q = q | child_q
            else:
                q = q & child_q
        if q is None:
            q = Q()
        if node.get("negate"):
            q = ~q
        return q
    return _condition(node.get("field"), node.get("op"), node.get("value"), fields)


def parse_json(text, fields):
    """Parse a JSON query string into a ``Q`` object."""
    if not text:
        return Q()
    try:
        node = json.loads(text)
    except (TypeError, ValueError):
        raise QueryError("invalid query")
    return parse(node, fields)
