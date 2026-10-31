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

