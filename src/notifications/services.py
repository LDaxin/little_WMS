"""Central notification creation (§6).

Views never build notification text themselves — they call this service, which
is the single place to translate the messages.
"""
from django.contrib.auth.models import User

from notifications.models import Notification


def notify(user, title, message="", link="", trigger_type=""):
    """Create an unread notification for one user."""
    return Notification.objects.create(
        user=user, title=title, message=message, link=link, trigger_type=trigger_type
    )


def notify_roles(organisation, codename, title, message="", link="", trigger_type=""):
    """Notify every user whose role in ``organisation`` holds ``codename``."""
    users = User.objects.filter(
        profiles__organisation=organisation,
        profiles__role__permissions__codename=codename,
    ).distinct()
    return [notify(user, title, message, link, trigger_type) for user in users]
