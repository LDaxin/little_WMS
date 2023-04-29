from django.db import models
import uuid
from softdelete.models import SoftDeleteObject

# Create your models here.

class UuidCode(SoftDeleteObject, models.Model):
   uuidCode = models.UUIDField(default = uuid.uuid4, editable = False, unique = True)
   code = models.CharField(max_length = 32, editable = False, unique = True, blank=True)

   def save(self, *args, **kwargs):
       if not self.code:
           code = str(self.uuidCode).replace("-", "")
           self.code = code
       super().save(*args, **kwargs)
    
   def __str__(self, *args, **kwargs):
       return self.code

