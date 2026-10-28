"""Middleware setting the active organisation on the request (§22)."""
from organisation.current import clear_current_organisation, set_current_organisation
from organisation.services import active_organisation


class ActiveOrganisationMiddleware:
    """Expose the active organisation to ``OrganisationManager``.

    The admin is skipped so it can see every organisation.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            return self.get_response(request)
        if request.user.is_authenticated:
            set_current_organisation(active_organisation(request))
        try:
            return self.get_response(request)
        finally:
            clear_current_organisation()
