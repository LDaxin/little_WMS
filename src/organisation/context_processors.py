"""Template context for the active organisation (§22)."""


def active_organisation(request):
    if not request.user.is_authenticated:
        return {}
    from organisation.services import active_organisation as get_active

    return {
        "active_organisation": get_active(request),
        "user_organisations": [
            profile.organisation
            for profile in request.user.profiles.select_related("organisation")
        ],
    }
