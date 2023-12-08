from django.db import models
from django.core import validators
from hub import models as hub_models
from hub.fields import SelfForeignKey
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from django import forms
from space.models import Space
# Create your models here.



class StorageType(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=200)
    lowerName = models.CharField(max_length=200, blank=True)
    symbol = models.CharField(max_length=20)
    matchables = SelfForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        self.lowerName = self.name.lower()
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "st" 
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.name

class Storage(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=200)
    typ = models.ForeignKey(StorageType, on_delete=models.CASCADE)
    parent = SelfForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    space = models.OneToOneField(Space,on_delete = models.CASCADE, related_name = "itemStorage", editable = False, blank = True, null = True)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "s0" 
            self.code = uCode
            uCode.save()
        if not self.space:
            space = Space()
            space.prefix = "s0"
            self.space = space
            space.save()
        super().save(*args, **kwargs)
    
    def __str__(self, *args, **kwargs):
        return self.name
