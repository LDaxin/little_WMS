from django.db import models
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from hub.fields import SelfForeignKey

# Create your models here.
class Location(SoftDeleteObject, models.Model):
    traditionalLand = models.CharField(max_length=50)
    traditionalCountry = models.CharField(max_length=50)
    traditionalCity = models.CharField(max_length=50)
    traditionalZipcode = models.CharField(max_length=15)
    traditionalStreet = models.CharField(max_length=200)
    traditionalStreetNumber = models.CharField(max_length=4)

    modernCoordinatesLongitude = models.FloatField(null=True)
    modernCoordinatesLatitude = models.FloatField(null=True)

    modernWhat3Words = models.CharField(max_length=100, null=True)
    modernWhat3WordsLang = models.CharField(max_length=50, null=True)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            self.code = "lo" + uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.traditionalLand + " " + self.traditionalCountry + " " + self.traditionalZipcode  + " " + self.traditionalStreet  + " " + self.traditionalStreetNumber

class Settings(SoftDeleteObject, models.Model):
    storageDepth = models.IntegerField(default = 5)

