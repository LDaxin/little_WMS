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


# The article list is a stock list: the queryset and the row object are
# ``Stock``; article-level columns reach through ``article__``.
ARTICLE_COLUMNS = [
    Column("name", _("Name"), "article__base__name", default=True),
    Column("code", _("Code"), "article__code__code", default=True),
    Column("type", _("Type"), "article__base__pType__name", default=True),
    Column("condition", _("Condition"), "article__zustand", renderer=BADGE, default=True),
    Column("location", _("Location"), "stored", level="stock", renderer=LOCATION,
           sortable=False, default=True),
    Column("quantity", _("Quantity"), "menge", level="stock", renderer=QUANTITY,
           default=True),
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


def selected_columns(list_type, cols, profile=None):
    """The columns for a ``cols`` string, the user's default, or the registry default."""
    if cols:
        chosen = [column(list_type, key) for key in cols.split(",")]
        chosen = [c for c in chosen if c]
        if chosen:
            return chosen
    if profile is not None:
        default = (getattr(profile, "list_columns", None) or {}).get(list_type)
        if default:
            chosen = [column(list_type, key) for key in default]
            chosen = [c for c in chosen if c]
            if chosen:
                return chosen
    return default_columns(list_type)


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


def order_by(queryset, list_type, sort):
    """Apply a ``sort`` parameter (``key`` or ``-key``) to a queryset.

    Falls back to the primary key so pagination is stable.
    """
    if not sort:
        return queryset.order_by("pk")
    descending = sort.startswith("-")
    path = sort_path(list_type, sort.lstrip("-"))
    if not path:
        return queryset.order_by("pk")
    return queryset.order_by(("-" if descending else "") + path)


def resolve_view_mode(request):
    """The effective list mode: ``table`` or ``cards`` (§ list-views).

    The ``mode`` parameter wins (the manual toggle); then the per-device
    list-view setting. The device comes from the view-mode setting, or the
    client hint when it is ``auto``.
    """
    from organisation.services import active_profile

    mode = request.GET.get("mode", "")
    if mode in ("table", "cards"):
        return mode
    profile = active_profile(request)
    setting = getattr(profile, "view_mode", "auto") or "auto"
    if setting == "mobile":
        device = "mobile"
    elif setting == "desktop":
        device = "desktop"
    else:
        device = "mobile" if request.headers.get("X-View-Mode") == "mobile" else "desktop"
    field = "list_view_mobile" if device == "mobile" else "list_view_desktop"
    default = "cards" if device == "mobile" else "table"
    return getattr(profile, field, default) or default


def is_mobile(request):
    """Whether the client counts as mobile (§ detail-view, § list-views).

    The view-mode setting wins (``mobile``/``desktop``); when it is ``auto`` the
    client hint decides.
    """
    from organisation.services import active_profile

    profile = active_profile(request)
    setting = getattr(profile, "view_mode", "auto") or "auto"
    if setting == "mobile":
        return True
    if setting == "desktop":
        return False
    return request.headers.get("X-View-Mode") == "mobile"


def resolve_detail_layout(request):
    """The effective detail layout: ``accordion`` or ``tabs`` (§ detail-view).

    Mobile always uses the accordion. On desktop the ``layout`` parameter wins
    (the manual toggle); then the ``detail_layout_desktop`` setting.
    """
    from organisation.services import active_profile

    if is_mobile(request):
        return "accordion"
    layout = request.GET.get("layout", "")
    if layout in ("accordion", "tabs"):
        return layout
    profile = active_profile(request)
    return getattr(profile, "detail_layout_desktop", "accordion") or "accordion"
