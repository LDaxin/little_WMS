# Generated by Django 4.2.6 on 2023-12-09 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('codeSystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('traditionalLand', models.CharField(max_length=50)),
                ('traditionalCountry', models.CharField(max_length=50)),
                ('traditionalCity', models.CharField(max_length=50)),
                ('traditionalZipcode', models.CharField(max_length=15)),
                ('traditionalStreet', models.CharField(max_length=200)),
                ('traditionalStreetNumber', models.CharField(max_length=4)),
                ('modernCoordinatesLongitude', models.FloatField(null=True)),
                ('modernCoordinatesLatitude', models.FloatField(null=True)),
                ('modernWhat3Words', models.CharField(max_length=100, null=True)),
                ('modernWhat3WordsLang', models.CharField(max_length=50, null=True)),
                ('code', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='codeSystem.uuidcode')),
            ],
            options={
                'permissions': (('can_undelete', 'Can undelete this object'),),
                'abstract': False,
            },
        ),
    ]