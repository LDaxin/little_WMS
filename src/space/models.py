from django.db import models
from softdelete.models import SoftDeleteObject
from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager

# Create your models here.

#TODO test if the query will return all stored things even the Container wenn the input is ready
class Space(SoftDeleteObject, models.Model):

    objects = SoftDeleteOrganisationManager()
    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    active = models.BooleanField(default = True)

    prefix = models.CharField(max_length = 2, editable = False)

    def __str__(self, *args, **kwargs):
        if self.prefix == "s0":
            return str(self.itemStorage.code.code)
        elif self.prefix == "a0":
            return str(self.itemArticle.code.code)
        else:
            return str(self.id)

