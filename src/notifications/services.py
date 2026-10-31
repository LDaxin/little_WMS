"""Central notification creation (§6).

Views never build notification text themselves — they call this service, which
is the single place to translate the messages.
"""
from django.contrib.auth.models import User

from notifications.models import Notification


def notify(user, title, message="", link="", trigger_type="", dedupe_key=""):
    """Create an unread notification for one user.

    When ``dedupe_key`` is given and the user already has an unread notification
    with that key, nothing is created (returns ``None``).
    """
    if dedupe_key and Notification.objects.filter(
        user=user, dedupe_key=dedupe_key, is_read=False
    ).exists():
        return None
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        link=link,
        trigger_type=trigger_type,
        dedupe_key=dedupe_key,
    )


def notify_roles(organisation, codename, title, message="", link="", trigger_type="", dedupe_key=""):
    """Notify every user whose role in ``organisation`` holds ``codename``."""
    users = User.objects.filter(
        profiles__organisation=organisation,
        profiles__role__permissions__codename=codename,
    ).distinct()
    return [
        notify(user, title, message, link, trigger_type, dedupe_key) for user in users
    ]
