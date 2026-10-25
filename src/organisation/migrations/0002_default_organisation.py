from django.db import migrations


def create_default_organisation(apps, schema_editor):
    Organisation = apps.get_model("organisation", "Organisation")
    Organisation.objects.get_or_create(
        pk=1, defaults={"name": "Default", "slug": "default"}
    )


def remove_default_organisation(apps, schema_editor):
    Organisation = apps.get_model("organisation", "Organisation")
    Organisation.objects.filter(pk=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("organisation", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_default_organisation,
            remove_default_organisation,
            elidable=True,
        ),
    ]
