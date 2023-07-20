from django.db import models
from softdelete.models import SoftDeleteObject


# Create your models here.
class ExportTemplate(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=200)
    fields = models.JSONField()
