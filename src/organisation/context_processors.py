"""Template context for the active organisation (§22) and sidebar (§12)."""


def _sidebar(profile):
    icon_desktop = getattr(profile, "icon_size_desktop", 28)
    icon_mobile = getattr(profile, "icon_size_mobile", 28)
    text_desktop = getattr(profile, "text_size_desktop", 15)
    text_mobile = getattr(profile, "text_size_mobile", 15)
    pos_desktop = getattr(profile, "sidebar_position_desktop", "left")
    pos_mobile = getattr(profile, "sidebar_position_mobile", "left")
    return {
        "icon_desktop": "%dpx" % icon_desktop,
        "icon_mobile": "%dpx" % icon_mobile,
        "text_desktop": "%dpx" % text_desktop,
        "text_mobile": "%dpx" % text_mobile,
        "dir_desktop": "row" if pos_desktop == "left" else "row-reverse",
        "dir_mobile": "row" if pos_mobile == "left" else "row-reverse",
    }


def active_organisation(request):
    if not request.user.is_authenticated:
        return {}
    from organisation.permissions import has_perm
    from organisation.services import active_organisation as get_active

    organisation = get_active(request)
    profile = request.user.profiles.filter(organisation=organisation).first()
    return {
        "active_organisation": organisation,
        "user_organisations": [
            profile.organisation
            for profile in request.user.profiles.select_related("organisation")
        ],
        "can_manage_roles": has_perm(request.user, "user.edit_role_all", organisation),
        "can_manage_notification_rules": has_perm(request.user, "notification.manage_rules_all", organisation),
        "sidebar": _sidebar(profile),
        "view_mode": getattr(profile, "view_mode", "auto"),
    }
