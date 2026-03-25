
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='amount',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

