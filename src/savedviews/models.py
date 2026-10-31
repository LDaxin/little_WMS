from django.db import models
from django.utils import timezone
from softdelete.models import SoftDeleteObject

import secrets

from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager


class SavedView(SoftDeleteObject, models.Model):
    """A named query-builder view (§10)."""

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="saved_views")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    typ = models.CharField(max_length=20, blank=True)
    query = models.JSONField(default=dict, blank=True)
    is_shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def applyUrl(self):
        return "/article/%s/?view=%s" % (self.typ, self.pk)


class ShareLink(models.Model):
    """A capability URL sharing a saved view (§10)."""

    ACCESS_MODES = [
        ("public", "Public (no login)"),
        ("guest", "Guest token"),
        ("internal", "Internal (organisation only)"),
    ]

    saved_view = models.ForeignKey(SavedView, on_delete=models.CASCADE, related_name="share_links")
    token = models.CharField(max_length=64, unique=True)
    access_mode = models.CharField(max_length=10, choices=ACCESS_MODES, default="public")
    expires_at = models.DateTimeField(null=True, blank=True)
    single_use = models.BooleanField(default=False)
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    password_hash = models.CharField(max_length=128, blank=True)
    created_by = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        if self.single_use and self.used_count >= 1:
            return False
        return True

    def __str__(self):
        return "Share link for %s" % self.saved_view
