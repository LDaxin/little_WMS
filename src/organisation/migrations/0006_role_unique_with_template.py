from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("organisation", "0005_role_templates"),
    ]

    operations = [
        # KI-020: a role created from a template may share the template's name
        migrations.AlterUniqueTogether(
            name="role",
            unique_together={("organisation", "name", "is_template")},
        ),
    ]
