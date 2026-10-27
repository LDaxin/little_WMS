from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AuditLog(models.Model):
    """Unified audit log for all objects (§32).

    One entry per action; ``content_object`` is the affected object (an Article
    for movements, since quantity lives on its ``Stock`` lines). The ``session``
    link (§11) is added once ``MovementSession`` exists.
    """

    user = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=30)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    changes = models.JSONField(default=dict, blank=True)
    undone = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp", "-id"]

    def __str__(self):
        return "%s %s" % (self.action, self.content_object)
