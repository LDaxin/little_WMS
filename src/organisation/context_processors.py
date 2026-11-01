"""Template context for the active organisation (§22) and sidebar (§12)."""

ICON_PX = {"small": "22px", "medium": "28px", "large": "34px"}
TEXT_REM = {"small": "0.8rem", "medium": "0.95rem", "large": "1.1rem"}


def _sidebar(profile):
    icon_desktop = getattr(profile, "icon_size_desktop", "medium")
    icon_mobile = getattr(profile, "icon_size_mobile", "medium")
    text_desktop = getattr(profile, "text_size_desktop", "medium")
    text_mobile = getattr(profile, "text_size_mobile", "medium")
    pos_desktop = getattr(profile, "sidebar_position_desktop", "left")
    pos_mobile = getattr(profile, "sidebar_position_mobile", "left")
    return {
        "icon_desktop": ICON_PX.get(icon_desktop, ICON_PX["medium"]),
        "icon_mobile": ICON_PX.get(icon_mobile, ICON_PX["medium"]),
        "text_desktop": TEXT_REM.get(text_desktop, TEXT_REM["medium"]),
        "text_mobile": TEXT_REM.get(text_mobile, TEXT_REM["medium"]),
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
