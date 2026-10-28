"""Permission catalog and checks (§3).

Permissions are ``object.action_scope`` strings, e.g. ``article.view_all``.
A ``Role`` stores them grouped by object: ``{"article": ["view_all", ...]}``.
"""

# object -> scopes / actions, straight from the §3 table.
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


def all_for(obj):
    """Every ``action_scope`` string for one object."""
    spec = PERMISSIONS[obj]
    return ["%s_%s" % (action, scope) for scope in spec["scopes"] for action in spec["actions"]]


def all_permissions():
    """Every permission string, e.g. ``article.view_all``."""
    return ["%s.%s" % (obj, perm) for obj in PERMISSIONS for perm in all_for(obj)]


def has_perm(user, perm):
    """Check a permission string like ``article.view_all`` (§3)."""
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    if user.is_superuser:
        return True
    profile = getattr(user, "profile", None)
    if profile is None or profile.role is None:
        return False
    obj, _, action = perm.partition(".")
    return action in profile.role.permissions.get(obj, [])


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
    from organisation.models import Role

    created = []
    for name, permissions in ROLE_TEMPLATES.items():
        role, was_created = Role.objects.get_or_create(
            organisation=organisation,
            name=name,
            defaults={"is_template": True, "permissions": permissions},
        )
        if was_created:
            created.append(role)
    return created
