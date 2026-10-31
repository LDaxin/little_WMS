from django.db import models
from softdelete.models import SoftDeleteObject

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
