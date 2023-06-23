from django.db import models
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from hub.fields import SelfForeignKey

# Create your models here.
class Settings(SoftDeleteObject, models.Model):
    storageDepth = models.IntegerField(default = 5)

