from datetime import timedelta

from django.db import models
from django.utils import timezone


class Organisation(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Audit log retention (§32): empty = keep forever, otherwise days to keep.
    log_retention_days = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Delete audit log entries older than this many days. Empty = keep forever.",
    )

    def retention_cutoff(self):
        """Datetime before which audit entries should be purged, or None (forever)."""
        if not self.log_retention_days:
            return None
        return timezone.now() - timedelta(days=self.log_retention_days)

    def __str__(self):
        return self.name


class Role(models.Model):
    """A named collection of permissions, per organisation (§3).

    ``permissions`` maps an object to a list of ``action_scope`` strings, e.g.
    ``{"article": ["view_all", "move_assigned"]}``.
    """

    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=50)
    is_template = models.BooleanField(default=False)
    permissions = models.JSONField(default=dict, blank=True)

    class Meta:
        # templates and real roles may share a name (KI-020)
        unique_together = ("organisation", "name", "is_template")

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """A user's membership in one organisation, with their role there (§3, §22).

    A user can belong to several organisations — one profile per organisation.
    """

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="profiles")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ("user", "organisation")

    def __str__(self):
        return "%s (%s)" % (self.user, self.role or "no role")
