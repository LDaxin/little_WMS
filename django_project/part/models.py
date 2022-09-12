import turtle
from django.db import models

from warehouse.models import Warehouse
from warehouse.models import Compartment
from container.models import Container

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)


class Template(models.Model):
    quantity_type_choices = (
        ("PC", "pieces"),
        ("g", "weight"),
        ("m", "length"),
    )

    name = models.CharField(max_length=200)

    weight = models.FloatField()

    quantity_type = models.CharField(max_length=4, choices=quantity_type_choices)

    length = models.FloatField()
    width = models.FloatField()
    depth = models.FloatField()

    tag = models.ManyToManyField(Tag)

    
class Part(models.Model):
    template = models.ForeignKey(Template, on_delete=models.RESTRICT)
    
    container = models.ForeignKey(Container, on_delete=models.SET_NULL, blank=True, null=True)
    compartment = models.ForeignKey(Compartment, on_delete=models.SET_NULL, blank=True, null=True)
    
    

    quantity = models.FloatField()

    tag = models.ManyToManyField(Tag, blank=True, null=True)

