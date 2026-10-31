from django.core.management.base import BaseCommand

from notifications.checks import run_checks
from notifications.services import notify_roles
from organisation.models import Organisation


class Command(BaseCommand):
    help = "Scan for due items and create notifications (§6)."

    def handle(self, *args, **options):
        created = 0
        for organisation in Organisation.objects.all():
            for finding in run_checks(organisation):
                results = notify_roles(
                    organisation,
                    "article_view_all",
                    finding.title,
                    finding.message,
                    finding.link,
                    finding.trigger_type,
                    finding.dedupe_key,
                )
                created += sum(1 for result in results if result is not None)
        self.stdout.write(self.style.SUCCESS("Notifications created: %d" % created))
