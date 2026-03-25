
from django.db import migrations, models
import django.db.models.deletion
import uuid

def dataTransfer(apps, schema_editor):
    Article = apps.get_model('article', 'Article')
    ArticleBase = apps.get_model('article', 'ArticleBase')
    UuidCode = apps.get_model('codeSystem', 'UuidCode')

    for article in Article.objects.all():
        uuidCode = uuid.uuid4()
        uCode = UuidCode.objects.create(prefix="ab", uuidCode=uuidCode, code="ab"+str(uuidCode).replace("-", ""))
        article.base = ArticleBase.objects.create(name=article.name, pType=article.pType, code=uCode)
        article.save()


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_article_amount'),
        ('codeSystem', '0002_alter_uuidcode_code'),
    ]

    operations = [
            migrations.CreateModel(
                name='ArticleBase',
                fields=[
                    ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                    ('name', models.CharField(max_length=20)),
                    ('pType', models.ForeignKey(blank=True, null=False, on_delete=django.db.models.deletion.CASCADE, to='article.articletype')),
                    ('code', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='codeSystem.uuidcode')),
                ],
                options={
                    'permissions': (('can_undelete', 'Can undelete this object'),),
                    'abstract': False,
                },
            ),
            migrations.AddField(
                model_name='article',
                name='base',
                field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article.articlebase'),
                preserve_default=False,
            ),
            migrations.RunPython(dataTransfer),
            migrations.AlterField(
                model_name='article',
                name='base',
                field=models.ForeignKey(blank=True, null=False, on_delete=django.db.models.deletion.CASCADE, to='article.articlebase'),
            ),
            migrations.RemoveField(
                model_name='article',
                name='pType',
            ),
            migrations.RemoveField(
                model_name='article',
                name='name',
            )

    ]
