from django.db import migrations


def parse_amount(apps, schema_editor):
    """Parse the free-text `amount` into `menge` + `mengeneinheit` (§18)."""
    Article = apps.get_model("article", "Article")
    changed = 0
    for article in Article.objects.all():
        raw = (article.amount or "").strip()
        parts = raw.split(" ", 1)
        if parts and parts[0].replace(".", "").replace(",", "").isdigit():
            article.menge = float(parts[0].replace(",", "."))
            article.mengeneinheit = parts[1] if len(parts) > 1 else ""
            article.save()
            changed += 1
    print("parse_amount: converted %d article(s)" % changed)


def reverse_parse_amount(apps, schema_editor):
    Article = apps.get_model("article", "Article")
    for article in Article.objects.all():
        if article.menge is not None:
            article.amount = ("%s %s" % (article.menge, article.mengeneinheit)).strip()
            article.save()


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0005_article_global_fields"),
    ]

    operations = [
        migrations.RunPython(parse_amount, reverse_parse_amount, elidable=True),
    ]
