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
