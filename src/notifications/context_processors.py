"""Expose the unread notification count to every template (§6)."""


def unread_notifications(request):
    if not request.user.is_authenticated:
        return {"unreadNotifications": 0}
    return {"unreadNotifications": request.user.notifications.filter(is_read=False).count()}
