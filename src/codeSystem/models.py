from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from softdelete.models import SoftDeleteObject
from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager

# Create your models here.

class UuidCode(SoftDeleteObject, models.Model):
   objects = SoftDeleteOrganisationManager()
   organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
   uuidCode = models.UUIDField(default = uuid.uuid4, editable = False, unique = True)
   code = models.CharField(_("Code"), max_length = 34, editable = False, unique = True, blank=True)
   prefix = models.CharField(_("Prefix"), max_length = 2, editable = False)
   used = models.BooleanField(_("Used"), default = True)

   def save(self, *args, **kwargs):
       if not self.code:
           code = self.prefix + str(self.uuidCode).replace("-", "")
           self.code = code
       super().save(*args, **kwargs)
    
   def __str__(self, *args, **kwargs):
       return self.code

