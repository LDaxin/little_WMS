"""Central notification creation (§6).

Views never build notification text themselves — they call this service, which
is the single place to translate the messages.
"""
from django.conf import settings
from django.contrib.auth.models import User

from notifications.models import Notification


def notify(user, title, message="", link="", trigger_type="", dedupe_key="", email=True):
    """Create an unread notification for one user.

    When ``dedupe_key`` is given and the user already has an unread notification
    with that key, nothing is created (returns ``None``). ``email`` controls
    whether the notification is also emailed.
    """
    if dedupe_key and Notification.objects.filter(
        user=user, dedupe_key=dedupe_key, is_read=False
    ).exists():
        return None
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        link=link,
        trigger_type=trigger_type,
        dedupe_key=dedupe_key,
    )
    if email:
        notify_email(user, title, message, link)
    return notification


def notify_email(user, title, message="", link=""):
    """Email a notification to the user (subject to verification + opt-out)."""
    if not user.email:
        return False
    from hub.mail import send

    body = message
    if link and settings.SITE_URL:
        link = settings.SITE_URL + link
    if link:
        body = (body + "\n\n" if body else "") + link
    return send(user.email, title, body, category="notifications")


def notify_roles(organisation, codename, title, message="", link="", trigger_type="", dedupe_key=""):
    """Notify every user whose role in ``organisation`` holds ``codename``."""
    users = User.objects.filter(
        profiles__organisation=organisation,
        profiles__role__permissions__codename=codename,
    ).distinct()
    return [
        notify(user, title, message, link, trigger_type, dedupe_key) for user in users
    ]


def notify_webhook(url, payload, secret=""):
    """POST a finding as JSON to a webhook URL (§6).

    Returns True on a 2xx response, False otherwise. Errors are logged, never
    raised, so a failing webhook cannot abort the trigger command.
    """
    import json
    import logging
    import urllib.request

    request = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), method="POST"
    )
    request.add_header("Content-Type", "application/json")
    if secret:
        request.add_header("X-Webhook-Secret", secret)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return 200 <= response.status < 300
    except Exception as error:  # noqa: BLE001 - a webhook must never abort the command
        logging.getLogger(__name__).warning("Webhook %s failed: %s", url, error)
        return False
