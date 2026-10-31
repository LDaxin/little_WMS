from django.db import models


class Notification(models.Model):
    """A per-user in-app notification (§6)."""

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="notifications")
    trigger_type = models.CharField(max_length=30, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    dedupe_key = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.title


class NotificationRule(models.Model):
    """A configurable notification rule (§6).

    Matched by ``trigger_type``; several active rules for the same trigger are
    all applied. A missing rule falls back to the default recipients.
    """

    TRIGGER_CHOICES = [
        ("expiry_date_reached", "Article expires soon"),
        ("maintenance_due", "Maintenance due"),
        ("minimum_stock_undercut", "Low stock"),
        ("return_overdue", "Loan return overdue"),
    ]

    organisation = models.ForeignKey(
        "organisation.Organisation", on_delete=models.CASCADE, related_name="notification_rules"
    )
    trigger_type = models.CharField(max_length=30, choices=TRIGGER_CHOICES)
    active = models.BooleanField(default=True)
    threshold_days = models.IntegerField(null=True, blank=True)
    notify_roles = models.ManyToManyField("organisation.Role", blank=True, related_name="notification_rules")
    notify_users = models.ManyToManyField("auth.User", blank=True, related_name="notification_rules")
    channel_in_app = models.BooleanField(default=True)
    channel_email = models.BooleanField(default=False)

    def recipients(self):
        """The users to notify: role members plus individual users."""
        from django.contrib.auth.models import User

        role_users = User.objects.filter(
            profiles__organisation=self.organisation,
            profiles__role__in=self.notify_roles.all(),
        )
        return (role_users | self.notify_users.all()).distinct()

    def __str__(self):
        return "%s (%s)" % (self.get_trigger_type_display(), self.organisation)
