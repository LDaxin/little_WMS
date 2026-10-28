from django.db import models
from softdelete.models import SoftDeleteObject
from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager


# Create your models here.
class ExportTemplate(SoftDeleteObject, models.Model):
    objects = SoftDeleteOrganisationManager()
    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    name = models.CharField(max_length=200)
    fields = models.JSONField()

