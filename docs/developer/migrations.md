# Migrations

Safe handling of database migrations. little_WMS is already in use, so every
schema change must be safe and reversible.

Reference: Lastenheft §7c (Migrations – Safe Handling) and §18 (Data Migration
& Transformation).

## Rules

1. **Every migration gets a backward migration** — no `makemigrations` without
   a verifiable rollback.
2. **Descriptive migration names** — `makemigrations --name "add_owner_field_to_article"`
   instead of `0003_auto`.
3. **Back up before every migration** — copy `data/wms.sqlite3`.
4. **No `--merge` without manual review** of the migrations to be merged.
5. **Data migrations** always with `elidable=True` and a check whether the data
   already exists.
6. **Test migrations** — forward + backward + forward again must be error-free.

## Workflow

All commands run inside the container (`docker compose exec web ...`).

```bash
# 1. Back up the database
cp data/wms.sqlite3 data/wms.sqlite3.backup_$(date +%Y%m%d_%H%M%S)

# 2. Create the migration
docker compose exec web python manage.py makemigrations --name "descriptive_name"

# 3. Apply it (forward)
docker compose exec web python manage.py migrate

# 4. Roll it back (backward)
docker compose exec web python manage.py migrate <app> <previous_migration>

# 5. Apply it again (forward)
docker compose exec web python manage.py migrate

# 6. Run the tests
docker compose exec web python manage.py test
```

The database lives in `data/wms.sqlite3` (mounted into the container as
`/app/data/wms.sqlite3`). `data/` is git-ignored, so backups stay local.

## Finding the previous migration

`showmigrations` lists every migration of an app and whether it is applied:

```bash
docker compose exec web python manage.py showmigrations <app>
```

Pick the migration directly before the one you want to roll back. To undo
`article/0003_restruckture_article`:

```bash
docker compose exec web python manage.py migrate article 0002_article_amount
```

## Data migrations

Schema migrations change the structure; data migrations change the data. Every
transformation is a data migration with `RunPython` and a `reverse_code`:

```python
from django.db import migrations


def forwards(apps, schema_editor):
    Article = apps.get_model("article", "Article")
    Article.objects.filter(amount__isnull=True).update(amount="1")


def backwards(apps, schema_editor):
    # Document any lossy rollback here.
    pass


class Migration(migrations.Migration):
    dependencies = [("article", "0003_restruckture_article")]
    operations = [
        migrations.RunPython(forwards, backwards, elidable=True),
    ]
```

- Use `apps.get_model(...)`, never import the model directly.
- `elidable=True` so the migration can be squashed later.
- Check whether the data already exists before writing it.
- If the rollback is lossy, document the loss in `backwards`.

## Migration tests

- Forward + backward + forward again must run without errors.
- Existing data must still be readable after the migration.
- Run the characterization tests after every migration (§7b).
