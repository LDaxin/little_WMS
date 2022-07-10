from django.db import models
from hub import models as hub_models

# Create your models here.

    
class Warehouse(models.Model):
    location = models.ForeignKey(hub_models.Location)
    active = models.BooleanField()
    name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=3)