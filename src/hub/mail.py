"""Central mail service (§30) and per-category email preferences (§6).

The only place that sends mail. When email is not configured it logs a warning
and skips, so callers never have to handle a missing SMTP server. This is also
the choke point where email-address verification and the per-category opt-out
are enforced.
"""
import logging

from django.conf import settings
from django.core.mail import send_mail as django_send_mail

from hub.models import EmailPreference

logger = logging.getLogger(__name__)


def is_subscribed(user, category):
    """Whether the user is subscribed to a category (default: yes)."""
    pref = EmailPreference.objects.filter(user=user, category=category).first()
    return pref is None or pref.subscribed


def set_subscription(user, category, subscribed):
    """Store the user's subscription for a category."""
    EmailPreference.objects.update_or_create(
        user=user, category=category, defaults={"subscribed": subscribed}
    )


def _recipient_subscribed(email, category):
    """Whether the address belongs to a user who is subscribed to the category.

    Addresses without a user (e.g. invitations to people without an account) are
    always considered subscribed.
    """
    from django.contrib.auth.models import User

    user = User.objects.filter(email=email).first()
    return user is None or is_subscribed(user, category)


def send(to, subject, body, require_verified=True, category=None):
    """Send a plain-text email. Returns True if sent, False if skipped.

    Unless ``require_verified`` is False, the recipient must have a verified
    address (double opt-in, §30); invitations are exempt. When ``category`` is
    given, a recipient who opted out of it is skipped.
    """
    if not getattr(settings, "EMAIL_CONFIGURED", False):
        logger.warning("Email not configured; skipping mail to %s (%s)", to, subject)
        return False
    if require_verified:
        from organisation.verification import is_verified

        if not is_verified(to):
            logger.warning("Email %s is not verified; skipping (%s)", to, subject)
            return False
    if category and not _recipient_subscribed(to, category):
        logger.warning("Email %s opted out of %s; skipping (%s)", to, category, subject)
        return False
    django_send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to])
    return True
