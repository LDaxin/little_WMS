from django.db import models
from storage.models import Stored
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from hub.fields import SelfForeignKey
from tag.models import Tag
from stored.models import Stored

# Create your models here.

"""
The Article model holds all articles and information about the Articles.

In der class Article is the unice Data is stored 
"""

class Unit(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=4)
    maximum = models.BigIntegerField(null=True, blank=True)
    minimum = models.BigIntegerField(default=0)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "un" 
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.name

#---------------------------------------------------------------------------
# The Article model is were the unice value is stored

class ArticleType(SoftDeleteObject, models.Model):
    tName = models.CharField(max_length=20)
    lowerName = models.CharField(max_length=200, blank=True)
    tSymbol = models.CharField(max_length=20)

    article_toggle_ref = models.BooleanField(default=False)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        self.lowerName = self.tName.lower()
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "at" 
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.tName

class Article(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=20)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)

    pType = models.ForeignKey(ArticleType, on_delete=models.PROTECT, blank=True)

    count = models.BigIntegerField(default=1)

    stored = models.ForeignKey(Stored, related_name= "stored", on_delete = models.SET_NULL, null=True, blank=True)

    ref = models.OneToOneField(Stored, on_delete = models.CASCADE, null=True, blank=True)

    tag = models.ManyToManyField(Tag, blank=True)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "a0" 
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)


    def __str__(self, *args, **kwargs):
        return self.name + " " + self.code.code
    
