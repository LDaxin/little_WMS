from django.db import models

# Create your models here.
class Location(models.Model):
    traditional_land = models.CharField(max_length=50)
    traditional_country = models.CharField(max_length=50)
    traditional_city = models.CharField(max_length=50)
    traditional_zipcode = models.CharField(max_length=15)
    traditional_street = models.CharField(max_length=200)
    traditional_street_number = models.CharField(max_length=4)

    modern_coordinates_longitude = models.FloatField(null=True)
    modern_coordinates_latitude = models.FloatField(null=True)

    modern_what3words = models.CharField(max_length=100, null=True)
    modern_what3words_lang = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.traditional_land + " " + self.traditional_country + " " + self.traditional_zipcode  + " " + self.traditional_street  + " " + self.traditional_street_number
