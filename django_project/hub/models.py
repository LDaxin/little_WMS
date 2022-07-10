from django.db import models

# Create your models here.
class Location(models.Model):
    traditional_land = models.CharField(max_length=50)
    tradutional_country = models.CharField(max_length=50)
    traditional_city = models.CharField(max_length=50)
    traditional_zipcode = models.IntegerField()

    modern_cordinates_longitudede = models.FloatField()
    modern_cordinates_latitude = models.FloatField()

    modern_what3words = models.CharField(max_length=50)
    modern_what3words_lang = models.CharField(max_length=50)