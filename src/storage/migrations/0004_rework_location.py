from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_tags'),
        ('location', '0004_rework_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='location.location'),
        ),
    ]
