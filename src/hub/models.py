from django.db import models
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from hub.fields import SelfForeignKey

# Create your models here.
class Settings(SoftDeleteObject, models.Model):
    REGISTRATION_POLICY_CHOICES = [
        ("open", "Open"),
        ("invite", "Invite only"),
        ("request", "Request"),
    ]

    storageDepth = models.IntegerField(default = 7)
    registration_policy = models.CharField(
        max_length=10, choices=REGISTRATION_POLICY_CHOICES, default="invite"
    )
    onboarding_completed = models.BooleanField(default=False)


class EmailPreference(models.Model):
    """A user's per-category email opt-out (§6).

    A missing row means subscribed, so the default is opt-out and new categories
    need no data migration.
    """

    CATEGORY_CHOICES = [
        ("notifications", "Notifications"),
        ("invitations", "Invitations"),
    ]

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="email_preferences")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    subscribed = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "category")

    def __str__(self):
        return "%s: %s" % (self.category, "subscribed" if self.subscribed else "unsubscribed")

