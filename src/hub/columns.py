"""Column registry for the list views (§ list-views).

The available columns per list type are defined here (code); the selection
(which columns, in which order) is data — a Saved View or the user's default.

A column's ``path`` is an ORM-style path relative to the row object. It is used
both to read the value (``__`` becomes attribute access) and, when ``sortable``,
to order the queryset.
"""
from django.utils.translation import gettext_lazy as _

# Renderer types — each maps to a template snippet in hub/columns/.
TEXT = "text"
BADGE = "badge"
LOCATION = "location"
QUANTITY = "quantity"
IMAGE = "image"


class Column:
    """One column of a list view."""

    def __init__(self, key, label, path, level="article", renderer=TEXT,
                 sortable=True, default=False):
        self.key = key
        self.label = label
        self.path = path
        self.level = level
        self.renderer = renderer
        self.sortable = sortable
        self.default = default

    def value(self, row):
        return resolve(row, self.path)


def resolve(obj, path):
    """Read ``path`` (``a__b``) from ``obj`` via attribute access."""
    for part in path.split("__"):
        obj = getattr(obj, part, None)
        if obj is None:
            return None
    return obj


# The article list is a stock list: the row object is a ``Stock``.
ARTICLE_COLUMNS = [
    Column("name", _("Name"), "article__base__name", default=True),
    Column("code", _("Code"), "article__code__code", default=True),
    Column("type", _("Type"), "article__base__pType__name", default=True),
    Column("condition", _("Condition"), "article__zustand", renderer=BADGE, default=True),
    Column("location", _("Location"), "stored", level="stock", renderer=LOCATION,
           sortable=False, default=True),
    Column("quantity", _("Quantity"), "menge", level="stock", renderer=QUANTITY, default=True),
    Column("expiry", _("Expiry"), "article__ablaufdatum"),
    Column("value", _("Purchase value"), "article__anschaffungswert"),
    Column("purchase_date", _("Purchase date"), "article__kaufdatum"),
    Column("weight", _("Weight"), "article__gewicht_gramm"),
    Column("unit", _("Unit"), "article__mengeneinheit", sortable=False),
    Column("tags", _("Tags"), "article__tags", sortable=False),
    Column("assignees", _("Assigned to"), "article__assigned_to", sortable=False),
    Column("minimum", _("Minimum stock"), "article__base__mindestbestand"),
    Column("ownership", _("Ownership"), "article__ownership", sortable=False),
    Column("note", _("Note"), "article__notiz", sortable=False),
]

# The storage list: the row object is a ``Storage``.
STORAGE_COLUMNS = [
    Column("name", _("Name"), "name", default=True),
    Column("code", _("Code"), "code__code", default=True),
    Column("type", _("Type"), "typ__name", default=True),
    Column("parent", _("Parent"), "parent__name", default=True),
    Column("location", _("Location"), "location", renderer=LOCATION,
           sortable=False, default=True),
    Column("contents", _("Contents"), "space__stocks", renderer=QUANTITY, sortable=False),
    Column("tags", _("Tags"), "tags", sortable=False),
]

LIST_TYPES = {
    "article": ARTICLE_COLUMNS,
    "storage": STORAGE_COLUMNS,
}


def columns(list_type):
    """Every available column for a list type."""
    return LIST_TYPES[list_type]


def default_columns(list_type):
    """The default columns for a list type."""
    return [c for c in LIST_TYPES[list_type] if c.default]


def column(list_type, key):
    """One column by key, or None."""
    for c in LIST_TYPES[list_type]:
        if c.key == key:
            return c
    return None


def sort_path(list_type, key):
    """The ORM path to order by for ``key``, or None when not sortable."""
    c = column(list_type, key)
    return c.path if c and c.sortable else None
