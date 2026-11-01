import json

from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder

from organisation.export import export_organisation
from organisation.models import Organisation


class Command(BaseCommand):
    help = "Export an organisation's inventory as JSON (§17)."

    def add_arguments(self, parser):
        parser.add_argument("slug")
        parser.add_argument("path")

    def handle(self, *args, **options):
        organisation = Organisation.objects.get(slug=options["slug"])
        data = export_organisation(organisation)
        with open(options["path"], "w") as handle:
            json.dump(data, handle, cls=DjangoJSONEncoder, indent=2)
        self.stdout.write(self.style.SUCCESS(
            "Exported %d objects to %s" % (len(data["objects"]), options["path"])
        ))
