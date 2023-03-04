from django.db import models
from hub import models as hub_models
from hub.countsystem import System
from softdelete.models import SoftDeleteObject
# Create your models here.

s = System()


#TODO test if the query will return all stored things even the Container wenn the input is ready
class Stored(SoftDeleteObject, models.Model):
    def __str__(self):
        mo = Warehouse.objects.filter(ref_id=self.id).first()
        if mo != None:
            code =  mo.name + " | " + mo.code 
            code = "Warehouse | " + code
        else:
            mo = Storage.objects.filter(ref_id=self.id).first()
            if mo != None:
                code = mo.warehouse.name + "/" + mo.name + " | " + mo.code  
                code = "Storage | " + code
            else:
                mo = Shelf.objects.filter(ref_id=self.id).first()
                if mo != None:
                    code = mo.storage.warehouse.name + "/" + mo.storage.name + "/" + mo.name + " | " + mo.code 
                    code = "Shelf | " + code
                else:
                    mo = Compartment.objects.filter(ref_id=self.id).first()
                    if mo != None:
                        code = mo.shelf.storage.warehouse.name + "/" + mo.shelf.storage.name + "/" + mo.shelf.name + "/" + mo.name +" | " + mo.code 
                        code = "Compartment | " + code
                    else:
                        try:
                            code = self.part_set.all().template.name
                        except:
                            code = "error"

        return code

class Warehouse(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=100)

    location = models.ForeignKey(hub_models.Location, on_delete=models.CASCADE)

    ref = models.OneToOneField(Stored,on_delete = models.CASCADE)
    code = models.CharField(max_length=16, unique=True, editable=False)


    def __str__(self):
        return self.name + " " + self.code

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

class Storage(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=100)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    ref = models.OneToOneField(Stored,on_delete = models.CASCADE)
    code = models.CharField(max_length=16, unique=True, editable=False)


    def __str__(self):
        return self.name + " " + self.code

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

class Shelf(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=100)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)

    rows = models.IntegerField()
    columns = models.IntegerField()
    
    ref = models.OneToOneField(Stored,on_delete = models.CASCADE)
    code = models.CharField(max_length=16, unique=True, editable=False)

    
    def __str__(self):
        return self.name + " " + self.code

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
        if not self.name:
            name = self.code[10:13].replace("0", "")
            self.name = name
        super().save(*args, **kwargs)

class Compartment(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=100)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)

    size_width = models.FloatField(null=True, blank=True)
    size_height = models.FloatField(null=True, blank=True)
    size_depth = models.FloatField(null=True, blank=True)

    row = models.IntegerField()
    colum = models.IntegerField()

    ref = models.OneToOneField(Stored,on_delete = models.CASCADE)
    code = models.CharField(max_length=16, unique=True, editable=False)

    
    def __str__(self):
        return self.name + " " + self.code

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

