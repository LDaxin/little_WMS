from django.db import migrations, models

from organisation.permissions import PERMISSIONS


def catalog_permissions():
    """The §3 catalogue as ``auth.Permission`` entries (area-prefixed codenames)."""
    entries = []
    for area, spec in PERMISSIONS.items():
        for scope in spec["scopes"]:
            for action in spec["actions"]:
                entries.append((
                    "%s_%s_%s" % (area, action, scope),
                    "%s: %s (%s)" % (area, action, scope),
                ))
    return entries


def copy_permissions(apps, schema_editor):
    """Map the old JSON ``permissions_data`` onto ``auth.Permission`` rows."""
    Role = apps.get_model("organisation", "Role")
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")

    content_type, _ = ContentType.objects.get_or_create(
        app_label="organisation", model="permissionarea"
    )
    by_codename = {}
    for area, spec in PERMISSIONS.items():
        for scope in spec["scopes"]:
            for action in spec["actions"]:
                code = "%s_%s_%s" % (area, action, scope)
                permission, _ = Permission.objects.get_or_create(
                    content_type=content_type,
                    codename=code,
                    defaults={"name": "%s: %s (%s)" % (area, action, scope)},
                )
                by_codename[code] = permission

    for role in Role.objects.all():
        for area, actions in (role.permissions_data or {}).items():
            for action_scope in actions:
                permission = by_codename.get("%s_%s" % (area, action_scope))
                if permission is not None:
                    role.permissions.add(permission)


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("organisation", "0008_alter_role_organisation_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PermissionArea",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ],
            options={
                "permissions": catalog_permissions(),
            },
        ),
        migrations.RenameField(
            model_name="role",
            old_name="permissions",
            new_name="permissions_data",
        ),
        migrations.AddField(
            model_name="role",
            name="permissions",
            field=models.ManyToManyField(blank=True, related_name="roles", to="auth.permission"),
        ),
        migrations.RunPython(copy_permissions, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="role",
            name="permissions_data",
        ),
    ]
