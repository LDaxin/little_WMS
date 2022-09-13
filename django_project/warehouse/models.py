from sys import prefix
from django.db import models
from hub import models as hub_models

# Create your models here.



class Warehouse(models.Model):
    location = models.ForeignKey(hub_models.Location, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)

    prefix = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class Storage(models.Model):

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    rows = models.IntegerField()
    columns = models.IntegerField()
    
    prefix = models.CharField(max_length=5)


class Compartment(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)

    size_width = models.FloatField(null=True, blank=True)
    size_height = models.FloatField(null=True, blank=True)
    size_depth = models.FloatField(null=True, blank=True)

    row = models.IntegerField()
    colum = models.IntegerField()

    prefix = models.CharField(max_length=6)



