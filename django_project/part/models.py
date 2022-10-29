from django.db import models
from warehouse.models import Warehouse
from warehouse.models import Compartment
from warehouse.models import Stored
#from maintenance.models import Plan
#from maintenance.models import Log


# Create your models here.

"""
The Part model holds all parts and information about the Parts.

In der class Part is the unice Data is stored 
"""

class Tag(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.parent != None:
            return str(self.parent) + "/" + self.name
        else:
            return self.name

#---------------------------------------------------------------------------
# The Part model is were the unice value is stored
class Part(models.Model):
    

    name = models.CharField(max_length=20) 

    description = models.TextField(null=True, blank=True)
    
    alias = models.CharField(max_length=400, null=True, blank=True)

    template = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    pType = models.CharField(max_length=10, default="base")

    width = models.FloatField(null=True, blank=True)
    depth = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    innerWidth = models.FloatField(null=True, blank=True)
    innerDepth = models.FloatField(null=True, blank=True)
    innerHeight = models.FloatField(null=True, blank=True)

    count = models.IntegerField(null=True, blank=True)

    weight = models.FloatField(null=True, blank=True)

    stored = models.ForeignKey(Stored, related_name= "stored", on_delete = models.SET_NULL, null=True, blank=True)

    ref = models.OneToOneField(Stored, on_delete = models.CASCADE, null=True, blank=True)

    tag = models.ManyToManyField(Tag, null=True, blank=True)

    code = models.CharField(max_length=16)


