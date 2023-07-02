from django.db import models
from softdelete.models import SoftDeleteObject
# Create your models here.

class LabelType(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=100)
    pixelX = models.IntegerField()
    pixelY = models.IntegerField()
    discription = models.TextField()

class LabelField(SoftDeleteObject, models.Model):
    positionX = models.IntegerField()
    positionY = models.IntegerField()
    fontSize = models.IntegerField()
    field = models.CharField(max_length=100)
    typ = models.CharField(max_length=100, choices=[('Storage', 'Storage'), ('Article', 'Article')])

class LabelImageField(SoftDeleteObject, models.Model):
    positionX = models.IntegerField()
    positionY = models.IntegerField()
    size = models.IntegerField()
    imageName = models.CharField(max_length=100)

class LabelText(SoftDeleteObject, models.Model):
    positionX = models.IntegerField()
    positionY = models.IntegerField()
    fontSize = models.IntegerField()
    text = models.CharField(max_length=200)
    
class Template(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=100)
    labelType = models.ForeignKey(LabelType, on_delete=models.CASCADE)
    description = models.TextField()

    fields = models.ManyToManyField(LableField)
    texts = models.ManyToManyField(LabelText)
    images = models.ManyToManyField(LabelImage)

class Printer(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    ip = models.CharField(max_length=15)
    typ = models.CharField(max_length=100, choices=[(("QL-500","QL-500"),("QL-550","QL-550"),("QL-560","QL-560"),("QL-570","QL-570"),("QL-580N","QL-580N"),("QL-650TD","QL-650TD"),("QL-700","QL-700"),("QL-710W","QL-710W"),("QL-720NW","QL-720NW"),("QL-800","QL-800"),("QL-810W","QL-810W"),("QL-820NWB","QL-820NWB"),("QL-1050","QL-1050"),("QL-1060N","QL-1060N"))])

'''
 Name      Printable px   Description
 12         106           12mm endless
 29         306           29mm endless
 38         413           38mm endless
 50         554           50mm endless
 54         590           54mm endless
 62         696           62mm endless
 102       1164           102mm endless
 17x54      165 x  566    17mm x 54mm die-cut
 17x87      165 x  956    17mm x 87mm die-cut
 23x23      202 x  202    23mm x 23mm die-cut
 29x42      306 x  425    29mm x 42mm die-cut
 29x90      306 x  991    29mm x 90mm die-cut
 39x90      413 x  991    38mm x 90mm die-cut
 39x48      425 x  495    39mm x 48mm die-cut
 52x29      578 x  271    52mm x 29mm die-cut
 62x29      696 x  271    62mm x 29mm die-cut
 62x100     696 x 1109    62mm x 100mm die-cut
 102x51    1164 x  526    102mm x 51mm die-cut
 102x152   1164 x 1660    102mm x 153mm die-cut
 d12         94 x   94    12mm round die-cut
 d24        236 x  236    24mm round die-cut
 d58        618 x  618    58mm round die-cut
'''
