from django.db import migrations

from organisation.permissions import ROLE_TEMPLATES


def create_templates(apps, schema_editor):
    Organisation = apps.get_model("organisation", "Organisation")
    Role = apps.get_model("organisation", "Role")
    for organisation in Organisation.objects.all():
        for name, permissions in ROLE_TEMPLATES.items():
            Role.objects.get_or_create(
                organisation=organisation,
                name=name,
                defaults={"is_template": True, "permissions": permissions},
            )


def remove_templates(apps, schema_editor):
    Role = apps.get_model("organisation", "Role")
    Role.objects.filter(is_template=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("organisation", "0004_role_userprofile"),
    ]

    operations = [
        migrations.RunPython(create_templates, remove_templates),
    ]
