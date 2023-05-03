from django.db import models
from storage.models import Stored
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from hub.fields import SelfForeignKey
from tag.models import Tag

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

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        self.lowerName = self.tName.lower()
        if not self.code:
            uCode = UuidCode()
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.tName

class ArticleTemplate(SoftDeleteObject, models.Model):

    name = models.CharField(max_length=20)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)

    description = models.TextField(null=True, blank=True)

    alias = models.CharField(max_length=400, null=True, blank=True)

    pType = models.ForeignKey(ArticleType, on_delete=models.PROTECT, blank=True)

    width = models.FloatField(null=True, blank=True)
    depth = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    innerWidth = models.FloatField(null=True, blank=True)
    innerDepth = models.FloatField(null=True, blank=True)
    innerHeight = models.FloatField(null=True, blank=True)

    weight = models.FloatField(null=True, blank=True)

    tag = models.ManyToManyField(Tag, blank=True)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.name


class Article(SoftDeleteObject, models.Model):
    template = models.ForeignKey(ArticleTemplate, on_delete=models.CASCADE, blank=True)
    count = models.IntegerField(default=1, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)

    stored = models.ForeignKey(Stored, related_name= "stored", on_delete = models.SET_NULL, null=True, blank=True)

    ref = models.OneToOneField(Stored, on_delete = models.CASCADE, null=True, blank=True)

    pTag = models.ManyToManyField(Tag, blank=True)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)


    def __str__(self, *args, **kwargs):
        return self.template.name + " " + self.code.code
    
