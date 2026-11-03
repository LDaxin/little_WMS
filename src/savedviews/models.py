from django.db import models
from softdelete.models import SoftDeleteObject

from hub.models import TokenisedModel
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
    sort = models.CharField(max_length=50, blank=True)
    columns = models.JSONField(default=list, blank=True)
    display_mode = models.CharField(max_length=10, blank=True)
    is_shared = models.BooleanField(default=False)
    show_on_dashboard = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def applyUrl(self):
        params = []
        if self.sort:
            params.append("sort=%s" % self.sort)
        if self.columns:
            params.append("cols=%s" % ",".join(self.columns))
        suffix = ("&" + "&".join(params)) if params else ""
        return "/article/%s/?view=%s%s" % (self.typ, self.pk, suffix)


class ShareLink(TokenisedModel):
    """A capability URL sharing a saved view (§10)."""

    ACCESS_MODES = [
        ("public", "Public (no login)"),
        ("guest", "Guest token"),
        ("internal", "Internal (organisation only)"),
    ]

    saved_view = models.ForeignKey(SavedView, on_delete=models.CASCADE, related_name="share_links")
    access_mode = models.CharField(max_length=10, choices=ACCESS_MODES, default="public")
    permissions = models.JSONField(default=list, blank=True)
    requires_confirmation = models.BooleanField(default=True)
    single_use = models.BooleanField(default=False)
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    password_hash = models.CharField(max_length=128, blank=True)
    created_by = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        if not self.is_active or self.is_expired():
            return False
        if self.single_use and self.used_count >= 1:
            return False
        return True

    def can(self, action):
        """Whether the link grants ``action`` (§10)."""
        return action in (self.permissions or [])

    def can_borrow(self):
        return self.can("borrow")

    def __str__(self):
        return "Share link for %s" % self.saved_view
