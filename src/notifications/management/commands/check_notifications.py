from django.conf import settings
from django.core.management.base import BaseCommand

from notifications.checks import run_checks
from notifications.models import NotificationRule
from notifications.services import notify, notify_email, notify_roles, notify_webhook
from organisation.models import Organisation


class Command(BaseCommand):
    help = "Scan for due items and create notifications (§6)."

    def handle(self, *args, **options):
        created = 0
        for organisation in Organisation.objects.all():
            for finding in run_checks(organisation):
                created += self._apply(organisation, finding)
        self.stdout.write(self.style.SUCCESS("Notifications created: %d" % created))

    def _apply(self, organisation, finding):
        """Notify the recipients of a finding, using the configured rules."""
        rules = NotificationRule.objects.filter(
            organisation=organisation, trigger_type=finding.trigger_type, active=True
        )
        if not rules.exists():
            results = notify_roles(
                organisation, "article_view_all",
                finding.title, finding.message, finding.link,
                finding.trigger_type, finding.dedupe_key,
            )
            return sum(1 for result in results if result is not None)

        created = 0
        for rule in rules:
            for user in rule.recipients():
                if rule.channel_in_app:
                    result = notify(
                        user, finding.title, finding.message, finding.link,
                        finding.trigger_type, finding.dedupe_key, email=rule.channel_email,
                    )
                    created += 1 if result is not None else 0
                elif rule.channel_email:
                    created += 1 if notify_email(
                        user, finding.title, finding.message, finding.link
                    ) else 0
            if rule.channel_webhook:
                notify_webhook(
                    rule.channel_webhook, self._payload(organisation, finding),
                    rule.webhook_secret,
                )
        return created

    def _payload(self, organisation, finding):
        """The JSON body for a webhook (§6)."""
        link = finding.link
        if link and settings.SITE_URL:
            link = settings.SITE_URL + link
        return {
            "trigger_type": finding.trigger_type,
            "title": finding.title,
            "message": finding.message,
            "link": link,
            "organisation": organisation.name,
        }
