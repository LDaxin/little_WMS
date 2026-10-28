from django.db import models


class MovementSession(models.Model):
    """A period of movement work by one user (§11).

    One open session per user; the session list and undo are built from the
    ``AuditLog`` entries linked to it.
    """

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at", "-id"]

    def __str__(self):
        return "Session %s (%s)" % (self.pk, self.user)
