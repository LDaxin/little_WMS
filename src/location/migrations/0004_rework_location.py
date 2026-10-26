from django.db import migrations, models


def copy_address(apps, schema_editor):
    """Convert the old rigid address fields to the new free-form ones (§28)."""
    Location = apps.get_model("location", "Location")
    for location in Location.objects.all():
        location.line1 = " ".join(
            p for p in [location.traditionalStreet, location.traditionalStreetNumber] if p
        )
        location.postal_code = location.traditionalZipcode or ""
        location.city = location.traditionalCity or ""
        location.state = location.traditionalCountry or ""
        location.country = (location.traditionalLand or "")[:2]
        location.latitude = location.modernCoordinatesLatitude
        location.longitude = location.modernCoordinatesLongitude
        location.save()


def reverse_copy_address(apps, schema_editor):
    Location = apps.get_model("location", "Location")
    for location in Location.objects.all():
        location.traditionalStreet = location.line1
        location.traditionalZipcode = location.postal_code
        location.traditionalCity = location.city
        location.traditionalCountry = location.state
        location.traditionalLand = location.country
        location.modernCoordinatesLatitude = location.latitude
        location.modernCoordinatesLongitude = location.longitude
        location.save()


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_fix_location_prefix'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='location',
            name='country',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='location',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='line1',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='location',
            name='line2',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='location',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='plus_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='location',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.RunPython(copy_address, reverse_copy_address, elidable=True),
        migrations.RemoveField(
            model_name='location',
            name='modernCoordinatesLatitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='modernCoordinatesLongitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='modernWhat3Words',
        ),
        migrations.RemoveField(
            model_name='location',
            name='modernWhat3WordsLang',
        ),
        migrations.RemoveField(
            model_name='location',
            name='traditionalCity',
        ),
        migrations.RemoveField(
            model_name='location',
            name='traditionalCountry',
        ),
        migrations.RemoveField(
            model_name='location',
            name='traditionalLand',
        ),
        migrations.RemoveField(
            model_name='location',
            name='traditionalStreet',
        ),
        migrations.RemoveField(
            model_name='location',
            name='traditionalStreetNumber',
        ),
        migrations.RemoveField(
            model_name='location',
            name='traditionalZipcode',
        ),
    ]
