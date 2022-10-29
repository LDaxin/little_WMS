from django.db import models
from hub import models as hub_models
# Create your models here.

#TODO test if the query will return all stored things even the Container wenn the input is ready
class Stored(models.Model):
    pass

class Warehouse(models.Model):
    location = models.ForeignKey(hub_models.Location, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)

    ref = models.OneToOneField(Stored,on_delete = models.CASCADE)
    code = models.CharField(max_length=16)


    def __str__(self):
        return self.name

class Storage(models.Model):

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    rows = models.IntegerField()
    columns = models.IntegerField()
    
    ref = models.OneToOneField(Stored,on_delete = models.CASCADE)
    code = models.CharField(max_length=16)


class Compartment(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)

    size_width = models.FloatField(null=True, blank=True)
    size_height = models.FloatField(null=True, blank=True)
    size_depth = models.FloatField(null=True, blank=True)

    row = models.IntegerField()
    colum = models.IntegerField()

    ref = models.OneToOneField(Stored,on_delete = models.CASCADE)
    code = models.CharField(max_length=16)
    


'''
class Container(models.Model):
    code = models.CharField(max_length=16)
    stored = models.ForeignKey(Stored, related_name= "stored", on_delete = models.SET_NULL, null=True, blank=True)

    innerWidth = models.FloatField(null=True, blank=True)
    innerDepth = models.FloatField(null=True, blank=True)
    innerHeight = models.FloatField(null=True, blank=True)

    ref = models.OneToOneField(Stored, on_delete = models.CASCADE)


-----------------------------------------------------------------------------------------------

    warehouse = models.OneToOneField(Warehouse, on_delete=models.CASCADE, null=True, blank=True)

    storage = models.OneToOneField(Storage, on_delete=models.CASCADE, null=True, blank=True)

    compartment = models.OneToOneField(Compartment, on_delete=models.CASCADE, null=True, blank=True)

    container = models.OneToOneField(Part, on_delete=models.CASCADE, null=True, blank=True)
    
    '''
