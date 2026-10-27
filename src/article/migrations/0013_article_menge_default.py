from django.db import migrations, models


def set_menge_default(apps, schema_editor):
    Article = apps.get_model("article", "Article")
    Article.objects.filter(menge__isnull=True).update(menge=1)


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0012_remove_article_standard_lagerplatz"),
    ]

    operations = [
        migrations.RunPython(set_menge_default, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="article",
            name="menge",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
    ]
