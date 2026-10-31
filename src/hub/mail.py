"""Central mail service (§30).

The only place that sends mail. When email is not configured it logs a warning
and skips, so callers never have to handle a missing SMTP server. This is also
the choke point where email-address verification will be enforced.
"""
import logging

from django.conf import settings
from django.core.mail import send_mail as django_send_mail

logger = logging.getLogger(__name__)


def send(to, subject, body):
    """Send a plain-text email. Returns True if sent, False if skipped."""
    if not getattr(settings, "EMAIL_CONFIGURED", False):
        logger.warning("Email not configured; skipping mail to %s (%s)", to, subject)
        return False
    django_send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to])
    return True
