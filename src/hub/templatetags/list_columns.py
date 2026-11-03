"""Template tags for the list views (§ list-views)."""
from django import template

register = template.Library()


@register.inclusion_tag("hub/columns/cell.html")
def cell(row, col):
    """Render one cell of a list row from the column registry."""
    return {"row": row, "col": col, "value": col.value(row)}


@register.filter
def space_path(space):
    from space.services import space_path as _space_path

    return _space_path(space) if space else ""


@register.filter
def condition_color(value):
    return {
        "gut": "success",
        "gebraucht": "secondary",
        "defekt": "danger",
        "reparatur": "warning",
    }.get(value, "secondary")


@register.filter
def condition_label(value):
    from article.models import ZUSTAND_CHOICES

    return dict(ZUSTAND_CHOICES).get(value, value)


@register.filter
def elided_page_range(page):
    """Page numbers around the current page, with gaps elided (§ list-views)."""
    return page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)


@register.filter
def has_level(columns, level):
    """Whether any of ``columns`` has the given level (§ list-views)."""
    return any(c.level == level for c in columns)
