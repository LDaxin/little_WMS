from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)


class Template(models.Model):
    weight = models.FloatField()
    tag = models.ForeignKey(Tag, on_delete=models.RESTRICT)

    
class Part(models.Model):
    template = models.ForeignKey(Template, on_delete=models.RESTRICT)
    tag = models.ManyToManyField(Tag)

