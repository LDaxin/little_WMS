from django.db import migrations


def fix_prefix(apps, schema_editor):
    """Location codes used the ArticleType prefix "at"; correct them to "l0" (§26)."""
    Location = apps.get_model("location", "Location")
    UuidCode = apps.get_model("codeSystem", "UuidCode")
    fixed = 0
    for location in Location.objects.all():
        if not location.code_id:
            continue
        code = UuidCode.objects.get(pk=location.code_id)
        if code.prefix == "at":
            code.prefix = "l0"
            code.code = "l0" + code.code[2:]
            code.save()
            fixed += 1
    print("fix_location_prefix: fixed %d location code(s)" % fixed)


def reverse_fix_prefix(apps, schema_editor):
    Location = apps.get_model("location", "Location")
    UuidCode = apps.get_model("codeSystem", "UuidCode")
    for location in Location.objects.all():
        if not location.code_id:
            continue
        code = UuidCode.objects.get(pk=location.code_id)
        if code.prefix == "l0":
            code.prefix = "at"
            code.code = "at" + code.code[2:]
            code.save()


class Migration(migrations.Migration):

    dependencies = [
        ("location", "0002_location_organisation"),
        ("codeSystem", "0003_uuidcode_organisation"),
    ]

    operations = [
        migrations.RunPython(fix_prefix, reverse_fix_prefix, elidable=True),
    ]
