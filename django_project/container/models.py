from sys import prefix
from django.db import models

# Create your models here.
class Template(models.Model):
    
    outer_size_width = models.FloatField()
    outer_size_height = models.FloatField()
    outer_size_depth = models.FloatField()

    inner_size_width = models.FloatField()
    inner_size_height = models.FloatField()
    inner_size_depth = models.FloatField()

    empty_weight = models.FloatField()

    prefix = models.CharField(max_length=6)


class container(models.Model):
    template = models.ForeignKey(Template)

    prefix = models.CharField(max_length=10)