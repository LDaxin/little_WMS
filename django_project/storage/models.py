from django.db import models
from django.core import validators
from hub import models as hub_models
from hub.countsystem import System
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from django import forms
# Create your models here.

s = System()



#TODO test if the query will return all stored things even the Container wenn the input is ready
class Stored(SoftDeleteObject, models.Model):
    def __str__(self, *args, **kwargs):
        return "Hallo"

codeStyleChoices=[('numeric', 'numeric'), ('alphaNumeric', 'alphaNumeric')]

class StorageType(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=200)
    lowerName = models.CharField(max_length=200, blank=True)
    symbol = models.CharField(max_length=20)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        self.lowerName = self.name.lower()
        if not self.code:
            uCode = UuidCode()
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)


class Storage(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=200)
    typ = models.ForeignKey(StorageType, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    ref = models.OneToOneField(Stored,on_delete = models.CASCADE)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)
    
