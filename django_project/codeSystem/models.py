from django.db import models
import uuid
from softdelete.models import SoftDeleteObject

# Create your models here.

class UuidCode(SoftDeleteObject, models.Model):
   uuidCode = models.UUIDField(default = uuid.uuid4, editable = False, unique = True)
   code = models.CharField(max_length = 34, editable = False, unique = True, blank=True)
   prefix = models.CharField(max_length = 2, editable = False)
   used = models.BooleanField(default = True)

   def save(self, *args, **kwargs):
       if not self.code:
           code = self.prefix + str(self.uuidCode).replace("-", "")
           self.code = code
       super().save(*args, **kwargs)
    
   def __str__(self, *args, **kwargs):
       return self.code

