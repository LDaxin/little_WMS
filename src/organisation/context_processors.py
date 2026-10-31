"""Template context for the active organisation (§22)."""


def active_organisation(request):
    if not request.user.is_authenticated:
        return {}
    from organisation.permissions import has_perm
    from organisation.services import active_organisation as get_active

    organisation = get_active(request)
    return {
        "active_organisation": organisation,
        "user_organisations": [
            profile.organisation
            for profile in request.user.profiles.select_related("organisation")
        ],
        "can_manage_roles": has_perm(request.user, "user.edit_role_all", organisation),
        "can_manage_notification_rules": has_perm(request.user, "notification.manage_rules_all", organisation),
    }
