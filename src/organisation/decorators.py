"""Permission decorators (§3)."""
from functools import wraps

from django.core.exceptions import PermissionDenied

from organisation.permissions import has_perm
from organisation.services import active_organisation


def require_perm(perm):
    """403 unless the user holds ``perm`` in their active organisation (§3)."""

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not has_perm(request.user, perm, active_organisation(request)):
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return wrapper

    return decorator
