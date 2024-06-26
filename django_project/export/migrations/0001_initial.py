# Generated by Django 4.2.6 on 2023-12-09 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExportTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('name', models.CharField(max_length=200)),
                ('fields', models.JSONField()),
            ],
            options={
                'permissions': (('can_undelete', 'Can undelete this object'),),
                'abstract': False,
            },
        ),
    ]
