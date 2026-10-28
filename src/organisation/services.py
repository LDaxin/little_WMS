"""Active-organisation handling (§22).

The active organisation is session-based; all work happens within it.
"""

SESSION_KEY = "active_organisation_id"


def active_organisation(request):
    """The organisation the request works in (§22).

    Session-based; falls back to the user's first membership, then the default
    organisation.
    """
    from organisation.models import Organisation

    org_id = request.session.get(SESSION_KEY)
    if org_id:
        organisation = Organisation.objects.filter(pk=org_id).first()
        if organisation is not None:
            return organisation
    if request.user.is_authenticated:
        profile = request.user.profiles.select_related("organisation").first()
        if profile is not None:
            return profile.organisation
    return Organisation.objects.get(pk=1)


def set_active_organisation(request, organisation):
    request.session[SESSION_KEY] = organisation.pk
    request.session.modified = True
