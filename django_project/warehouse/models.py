from sys import prefix
from django.db import models
from hub import models as hub_models

# Create your models here.



class Warehouse(models.Model):
    location = models.ForeignKey(hub_models.Location, on_delete=models.CASCADE)
    active = models.BooleanField()
    name = models.CharField(max_length=100)

    prefix = models.CharField(max_length=5)


class Storage(models.Model):

    compartments = models.IntegerField()

    rows = models.IntegerField()
    columns = models.IntegerField()
    
    prefix = models.CharField(max_length=5)

class Compartment(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)

    size_width = models.FloatField()
    size_height = models.FloatField()
    size_depth = models.FloatField()

    row = models.IntegerField()
    colum = models.IntegerField()

    prefix = models.CharField(max_length=6)