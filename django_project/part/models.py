from django.db import models
from warehouse.models import Stored
from hub.countsystem import System
#from maintenance.models import Plan
#from maintenance.models import Log


# Create your models here.

"""
The Part model holds all parts and information about the Parts.

In der class Part is the unice Data is stored 
"""

s = System()


class Tag(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.parent != None:
            return str(self.parent) + "/" + self.name
        else:
            return self.name

class Unit(models.Model):
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=4)
    maximum = models.BigIntegerField(null=True, blank=True)
    minimum = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name

#---------------------------------------------------------------------------
# The Part model is were the unice value is stored

class Type(models.Model):
    tName = models.CharField(max_length=20)
    tShort = models.CharField(max_length=2)
    tSymbol = models.CharField(max_length=20)

    name = models.BooleanField(default=True, editable=False)
    unit = models.BooleanField(default=True, editable=False)
    count = models.BooleanField(default=True, editable=False)
    stored = models.BooleanField(default=True, editable=False)


    description = models.BooleanField(default=True)
    tag = models.BooleanField(default=True)
    alias = models.BooleanField(default=True)

    width = models.BooleanField(default=False)
    depth = models.BooleanField(default=False)
    height = models.BooleanField(default=False)

    innerWidth = models.BooleanField(default=False)
    innerDepth = models.BooleanField(default=False)
    innerHeight = models.BooleanField(default=False)

    ref = models.BooleanField(default=False)

    weight = models.BooleanField(default=False)
    volume = models.BooleanField(default=False)
    length = models.BooleanField(default=False)
    pTag = models.BooleanField(default=False)


    def __str__(self):
        return self.tName

class Template(models.Model):

    name = models.CharField(max_length=20) 
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)

    description = models.TextField(null=True, blank=True)
    
    alias = models.CharField(max_length=400, null=True, blank=True)

    pType = models.ForeignKey(Type, on_delete=models.PROTECT, blank=True)

    width = models.FloatField(null=True, blank=True)
    depth = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    innerWidth = models.FloatField(null=True, blank=True)
    innerDepth = models.FloatField(null=True, blank=True)
    innerHeight = models.FloatField(null=True, blank=True)

    weight = models.FloatField(null=True, blank=True)

    tag = models.ManyToManyField(Tag, blank=True)

    code = models.CharField(max_length=16, unique=True, editable=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.code:
            if len(self.name) < 5:
                name_part = self.name + "00000"[len(self.name):]
            else:
                name_part = self.name[:5]
            code = self.pType.tShort + name_part.upper().replace(" ", "")
            try:
                number = Template.objects.filter(code__startswith=code).last().code[7:9]
                number = s.up(number)
                code = code + number + "0000000"
            except AttributeError:
                code = code + "000000000"
            self.code = code

        super().save(*args, **kwargs)


class Part(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE, blank=True)
    count = models.IntegerField(default=1, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)

    stored = models.ForeignKey(Stored, related_name= "stored", on_delete = models.SET_NULL, null=True, blank=True)

    ref = models.OneToOneField(Stored, on_delete = models.CASCADE, null=True, blank=True)

    pTag = models.ManyToManyField(Tag, blank=True)

    code = models.CharField(max_length=16, unique=True, editable=False)

    deleted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.template.name + " " + self.code
    
    def save(self, *args, **kwargs):
        if not self.code:
            code = self.template.code[:9]
            try:
                number = Part.objects.filter(code__startswith=code).last().code[9:]
                number = s.up(number)
                code = code + number
            except AttributeError:
                code = code + "0000001"

            self.code = code

        super().save(*args,**kwargs)

