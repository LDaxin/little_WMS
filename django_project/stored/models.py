from django.db import models
from softdelete.models import SoftDeleteObject

# Create your models here.

#TODO test if the query will return all stored things even the Container wenn the input is ready
class Stored(SoftDeleteObject, models.Model):

    active = models.BooleanField(default = True)

    def __str__(self, *args, **kwargs):
        return str(self.id)

