"""DRF permissions coupled to the role system (§3, §7a)."""
from rest_framework.permissions import BasePermission

from organisation.permissions import has_perm
from organisation.services import active_organisation

ACTION_BY_METHOD = {
    "GET": "view",
    "HEAD": "view",
    "OPTIONS": "view",
    "POST": "create",
    "PUT": "edit",
    "PATCH": "edit",
    "DELETE": "delete",
}


class RolePermission(BasePermission):
    """Gate an endpoint by the role system: method → action, viewset → area."""

    def has_permission(self, request, view):
        area = getattr(view, "permission_area", None)
        if area is None:
            return True
        action = ACTION_BY_METHOD.get(request.method, "view")
        return has_perm(
            request.user, "%s.%s_all" % (area, action), active_organisation(request)
        )
