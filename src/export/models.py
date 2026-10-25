from django.db import models
from softdelete.models import SoftDeleteObject


# Create your models here.
class ExportTemplate(SoftDeleteObject, models.Model):
    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    fields = models.JSONField()

