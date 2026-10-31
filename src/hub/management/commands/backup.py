import os

from django.conf import settings
from django.core.management.base import BaseCommand

from hub.backup import create_backup


class Command(BaseCommand):
    help = "Create a full database backup (§17)."

    def add_arguments(self, parser):
        parser.add_argument("path", nargs="?", default="")

    def handle(self, *args, **options):
        path = options["path"] or os.path.join(
            os.path.dirname(settings.DATABASES["default"]["NAME"]), "backup.sqlite3"
        )
        if os.path.exists(path):
            os.remove(path)
        create_backup(path)
        self.stdout.write(self.style.SUCCESS("Backup written to %s" % path))
