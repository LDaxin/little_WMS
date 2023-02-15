from django.db import models
from hub import models as hub_models
from hub.countsystem import System
# Create your models here.

s = System()


#TODO test if the query will return all stored things even the Container wenn the input is ready
class Stored(models.Model):
    def __str__(self):
        mo = Warehouse.objects.filter(ref_id=self.id).first()
        if mo != None:
            code =  mo.location.name + "/" + mo.name + " | " + mo.code 
            code = "Warehouse | " + code
        else:
            mo = Storage.objects.filter(ref_id=self.id).first()
            if mo != None:
                code = mo.warehouse.location.name + "/" + mo.warehouse.name + "/" + mo.name + " | " + mo.code  
                code = "Storage | " + code
            else:
                mo = Shelf.objects.filter(ref_id=self.id).first()
                if mo != None:
                    code =  mo.storage.warehouse.location.name + "/" + mo.storage.warehouse.name + "/" + mo.storage.name + "/" + mo.name + " | " + mo.code 
                    code = "Shelf | " + code
                else:
                    mo = Compartment.objects.filter(ref_id=self.id).first()
                    if mo != None:
                        code =  mo.shelf.storage.warehouse.location.name + "/" + mo.shelf.storage.warehouse.name + "/" + mo.shelf.storage.name + "/" + mo.shelf.name + "/" + mo.name +" | " + mo.code 
                        code = "Compartment | " + code
                    else:
                        code = "Error"
        return code

class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    location = models.ForeignKey(hub_models.Location, on_delete=models.CASCADE)

    ref = models.OneToOneField(Stored,on_delete = models.CASCADE)
    code = models.CharField(max_length=16, unique=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            code = "ST"
            try:
                number = Warehouse.objects.last().code[2:6]
                number = s.up(number)
                code = code + number + "0000000000"
            except AttributeError:
                code = code + "00000000000000"
            self.code = code
        super().save(*args, **kwargs)

class Storage(models.Model):
    name = models.CharField(max_length=100)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    ref = models.OneToOneField(Stored,on_delete = models.CASCADE)
    code = models.CharField(max_length=16, unique=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            code = self.warehouse.code[:6]
            try:
                number = Storage.objects.filter(code__startswith=code).last().code[6:10]
                number = s.up(number)
                code = code + number + "000000"

            except AttributeError:
                code = code + "0001000000"
            self.code = code
        super().save(*args, **kwargs)

class Shelf(models.Model):
    name = models.CharField(max_length=100)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)

    rows = models.IntegerField()
    columns = models.IntegerField()
    
    ref = models.OneToOneField(Stored,on_delete = models.CASCADE)
    code = models.CharField(max_length=16, unique=True, editable=False)
    
    def save(self, *args, **kwargs):
        if not self.code:
            code = self.storage.code[:10] 
            try:
                number = Shelf.objects.filter(code__startswith=code).last().code[10:13]
                number = s.up(number)
                code = code + number + "000"

            except AttributeError:
                code = code + "001000"
            self.code = code
        super().save(*args, **kwargs)

class Compartment(models.Model):
    name = models.CharField(max_length=100)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)

    size_width = models.FloatField(null=True, blank=True)
    size_height = models.FloatField(null=True, blank=True)
    size_depth = models.FloatField(null=True, blank=True)

    row = models.IntegerField()
    colum = models.IntegerField()

    ref = models.OneToOneField(Stored,on_delete = models.CASCADE)
    code = models.CharField(max_length=16, unique=True, editable=False)
    

    def save(self, *args, **kwargs):
        if not self.code:
            code = self.shelf.code[:13] 
            try:
                number = Compartment.objects.filter(code__startswith=code).last().code[13:]
                number = s.up(number)
                code = code + number 

            except AttributeError:
                code = code + "001"
            self.code = code
        super().save(*args, **kwargs)

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
