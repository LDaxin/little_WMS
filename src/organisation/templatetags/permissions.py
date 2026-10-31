"""Template filters for permission checks (§3)."""
from django import template

from organisation.current import get_current_organisation
from organisation.permissions import has_perm as _has_perm

register = template.Library()


@register.filter
def has_perm(user, perm):
    """``{% if user|has_perm:"article.view_all" %}``."""
    return _has_perm(user, perm, get_current_organisation())
