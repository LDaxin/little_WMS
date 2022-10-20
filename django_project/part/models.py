from django.db import models
from warehouse.models import Warehouse
from warehouse.models import Compartment
from maintenance.models import Plan
from maintenance.models import Log


# Create your models here.

"""
The Part model holds all parts and information about the Parts.

In der class Part is the unice Data is stored 
"""

class Tag(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

#---------------------------------------------------------------------------
# The Part model is were the unice value is stored
class Part(models.Model):
    
    name = models.CharField(max_length=20) 
    
    width = models.FloatField()
    depth = models.FloatField()
    height = models.FloatField()

    
    weight = models.FloatField()

    stored = models.BooleanField()

    tag = models.ManyToManyField(Tag)

    code = models.CharField(max_length=16)

class Template(models.Model):

    name = models.CharField(max_length=20) 
    
    width = models.FloatField()
    depth = models.FloatField()
    height = models.FloatField()

    weight = models.FloatField()

    tag = models.ManyToManyField(Tag)

    templateCode = models.CharField(max_length=16)


#---------------------------------------------------------------------------
class ContainerTemplate(models.Model):
    template = models.OneToOneField(Template, on_delete=models.CASCADE)

    innerWidth = models.FloatField()
    innerDepth = models.FloatField()
    innerHeight = models.FloatField()


class Container(models.Model):
    base = models.ForeignKey(ContanerTemplate, on_delete=models.SET_NULL, null=True)
    part = models.OneToOneField(Part, on_delete=models.CASCADE)

    innerWidth = models.FloatField()
    innerDepth = models.FloatField()
    innerHeight = models.FloatField()


#---------------------------------------------------------------------------
class DeviceTempalate(models.Model):
    template = models.OneToOneField(Template, on_delete=models.CASCADE)

    maintenancePlan = models.ForeignKey(Plan, on_delete=models.CASCADE)

class Device(models.Model):
    base = models.ForeignKey(DeviceTemplate, on_delete=models.SET_NULL, null=True)
    part = models.OneToOneField(Part, on_delete=models.CASCADE)

    maintenancePlan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    maintenanceLog = models.ManyToManyField(Log)

#---------------------------------------------------------------------------
class FoodTemplate(models.Model):
    template = models.OneToOneField(Template, on_delete=models.CASCADE)
    
    ean8 = models.BooleanField()
    ean13 = models.BooleanField()

    ean = models.IntegerField()


class Food(models.Model):
    base = models.ForeignKey(FoodTemplate, on_delete=models.SET_NULL, null=True)
    part = models.OneToOneField(Part, on_delete=models.CASCADE)

    exprorationDate = models.DateTimeField()

    ean8 = models.BooleanField()
    ean13 = models.BooleanField()

    ean = models.IntegerField()


#---------------------------------------------------------------------------
class SetTemplate(models.Modle):
    template = models.OneToOneField(Template, on_delete=models.CASCADE)

    parts = models.ManyToManyField(Part)


class Set(models.Model):
    base = models.ForeignKey(FoodTemplate, on_delete=models.SET_NULL, null=True)
    part = models.OneToOneField(Part, on_delete=models.CASCADE)

    parts = models.ManyToManyField(Part)


