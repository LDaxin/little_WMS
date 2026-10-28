from django.core.management.base import BaseCommand

from audit.models import AuditLog
from organisation.models import Organisation


class Command(BaseCommand):
    help = "Delete audit log entries older than each organisation's retention (§32)."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true",
                            help="Report what would be deleted without deleting.")

    def handle(self, *args, **options):
        total = 0
        for org in Organisation.objects.all():
            cutoff = org.retention_cutoff()
            if cutoff is None:
                continue
            qs = AuditLog.objects.filter(organisation=org, timestamp__lt=cutoff)
            count = qs.count()
            if not options["dry_run"]:
                qs.delete()
            total += count
            self.stdout.write("%s: %s entries" % (org, count))
        suffix = " (dry run)" if options["dry_run"] else ""
        self.stdout.write("Total: %s entries%s" % (total, suffix))
