import json

from django.core.management.base import BaseCommand

from organisation.export import import_organisation


class Command(BaseCommand):
    help = "Import an organisation from a JSON export (§17)."

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("--name", default="")

    def handle(self, *args, **options):
        with open(options["path"]) as handle:
            data = json.load(handle)
        organisation = import_organisation(data, name=options["name"] or None)
        self.stdout.write(self.style.SUCCESS("Imported organisation %s" % organisation))
