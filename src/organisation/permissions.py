"""Permission catalog and checks (§3).

The catalogue is declared here and materialised as Django ``auth.Permission``
entries on ``organisation.PermissionArea`` (area-prefixed codenames like
``article_view_all``). A ``Role`` links to those permissions via M2M.
"""

# area -> scopes / actions, straight from the §3 table.
PERMISSIONS = {
    "article": {"scopes": ["assigned", "all"], "actions": ["view", "create", "edit", "delete", "move"]},
    "storage": {"scopes": ["assigned", "all"], "actions": ["view", "create", "edit", "delete"]},
    "occasion": {"scopes": ["assigned", "all"], "actions": ["view", "create", "edit", "delete", "manage_packlist"]},
    "tag": {"scopes": ["all"], "actions": ["view", "create", "edit", "delete"]},
    "location": {"scopes": ["all"], "actions": ["view", "create", "edit", "delete"]},
    "code": {"scopes": ["all"], "actions": ["view", "create", "delete", "export"]},
    "user": {"scopes": ["all"], "actions": ["view", "invite", "edit_role", "deactivate"]},
    "settings": {"scopes": ["all"], "actions": ["view", "edit"]},
    "notification": {"scopes": ["all"], "actions": ["view", "manage_rules"]},
    "export": {"scopes": ["all"], "actions": ["csv", "qr_sheet"]},
    "calendar": {"scopes": ["all"], "actions": ["view", "create_entries"]},
    "trash": {"scopes": ["all"], "actions": ["view", "restore", "delete_forever"]},
}


def action_for(action, scope):
    """``action_scope`` string, e.g. ``view_all``."""
    return "%s_%s" % (action, scope)


def all_for(obj):
    """Every ``action_scope`` string for one area."""
    spec = PERMISSIONS[obj]
    return [action_for(action, scope) for scope in spec["scopes"] for action in spec["actions"]]


def all_codenames():
    """Every permission codename, e.g. ``article_view_all``."""
    return ["%s_%s" % (obj, perm) for obj in PERMISSIONS for perm in all_for(obj)]


def codename(perm):
    """``article.view_all`` -> ``article_view_all``."""
    area, _, action_scope = perm.partition(".")
    return "%s_%s" % (area, action_scope)


def template_codenames(permissions):
    """``{"article": ["view_all"]}`` -> ``["article_view_all"]``."""
    return [
        "%s_%s" % (area, action_scope)
        for area, action_scopes in permissions.items()
        for action_scope in action_scopes
    ]


def _profile(user, organisation=None):
    """The user's membership profile, optionally for a specific organisation."""
    profiles = user.profiles.all()
    if organisation is not None:
        return profiles.filter(organisation=organisation).first()
    return profiles.first()


def has_perm(user, perm, organisation=None):
    """Check a permission string like ``article.view_all`` (§3).

    Evaluated against the user's role in ``organisation`` (or their first
    membership when none is given).
    """
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    if user.is_superuser:
        return True
    profile = _profile(user, organisation)
    if profile is None or profile.role is None:
        return False
    return profile.role.permissions.filter(codename=codename(perm)).exists()


def role_codenames(user, organisation=None):
    """The permission codenames granted by the user's role in ``organisation``."""
    if user is None or not getattr(user, "is_authenticated", False):
        return set()
    profile = _profile(user, organisation)
    if profile is None or profile.role is None:
        return set()
    return set(profile.role.permissions.values_list("codename", flat=True))


def has_scope(user, area, action, organisation=None, obj=None):
    """Scope-aware check (§3).

    ``_all`` grants the action; ``_assigned`` grants it only when ``obj`` is
    assigned to the user (or ``obj is None``, for list/aggregate access).
    """
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    if user.is_superuser:
        return True
    codenames = role_codenames(user, organisation)
    if "%s_%s_all" % (area, action) in codenames:
        return True
    if "%s_%s_assigned" % (area, action) in codenames:
        return obj is None or user in obj.assigned_to.all()
    return False


def is_assigned_only(user, area, action, organisation=None):
    """True when the role has the ``_assigned`` scope but not ``_all``."""
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    if user.is_superuser:
        return False
    codenames = role_codenames(user, organisation)
    return (
        "%s_%s_assigned" % (area, action) in codenames
        and "%s_%s_all" % (area, action) not in codenames
    )


# Pre-configured role templates (§3). Not active, just suggestions.
ROLE_TEMPLATES = {
    "Full Access": {obj: all_for(obj) for obj in PERMISSIONS},
    "Family": {obj: all_for(obj) for obj in PERMISSIONS},
    "Warehouse Team": {
        "article": ["view_all", "edit_all", "move_all"],
        "storage": ["view_all"],
        "occasion": ["view_all", "manage_packlist_all"],
        "export": ["csv_all", "qr_sheet_all"],
        "calendar": ["view_all"],
    },
    "Read Only": {
        "article": ["view_all"],
        "storage": ["view_all"],
        "occasion": ["view_all"],
        "calendar": ["view_all"],
    },
    "Occasion Manager": {
        "article": ["view_all"],
        "occasion": all_for("occasion"),
        "calendar": all_for("calendar"),
        "export": ["qr_sheet_all"],
    },
    "Section Lead": {
        "article": ["view_all", "edit_all", "move_assigned"],
        "storage": ["view_all"],
        "occasion": ["view_assigned", "manage_packlist_all"],
    },
}


def ensure_role_templates(organisation):
    """Create the pre-configured role templates for an organisation (§3)."""
    from django.contrib.auth.models import Permission

    from organisation.models import Role

    created = []
    for name, permissions in ROLE_TEMPLATES.items():
        role, was_created = Role.objects.get_or_create(
            organisation=organisation, name=name, defaults={"is_template": True}
        )
        if was_created:
            role.permissions.set(
                Permission.objects.filter(codename__in=template_codenames(permissions))
            )
            created.append(role)
    return created
