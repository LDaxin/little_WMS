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
