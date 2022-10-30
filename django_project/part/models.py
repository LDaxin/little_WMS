from django.db import models
from warehouse.models import Warehouse
from warehouse.models import Compartment
from warehouse.models import Stored
#from maintenance.models import Plan
#from maintenance.models import Log


# Create your models here.

"""
The Part model holds all parts and information about the Parts.

In der class Part is the unice Data is stored 
"""

class Tag(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.parent != None:
            return str(self.parent) + "/" + self.name
        else:
            return self.name

#---------------------------------------------------------------------------
# The Part model is were the unice value is stored

value_list = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

class Template(models.Model):
    type_list = [
            ("BA", "BA"),
            ("CO", "CO"),
            ]

    name = models.CharField(max_length=20) 

    description = models.TextField(null=True, blank=True)
    
    alias = models.CharField(max_length=400, null=True, blank=True)

    pType = models.CharField(max_length=10, choices=type_list, default="BA")

    width = models.FloatField(null=True, blank=True)
    depth = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    innerWidth = models.FloatField(null=True, blank=True)
    innerDepth = models.FloatField(null=True, blank=True)
    innerHeight = models.FloatField(null=True, blank=True)

    weight = models.FloatField(null=True, blank=True)

    tag = models.ManyToManyField(Tag, blank=True)

    code = models.CharField(max_length=16, unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.code:
            if len(self.name) < 5:
                name_part = self.name + "00000"[len(self.name):]
            else:
                name_part = self.name[:5]
            code = self.pType + name_part.upper() 
            try:
                number = Template.objects.filter(code__startswith=code).last().code[7:-7]
                first = value_list.index(number[1:])
                second = value_list.index(number[:1])
                first += 1
                if first == 36:
                    first = 0
                    secont =+ 1

                code = code + value_list[second] + value_list[first] + "0000000"
            except AttributeError:
                code = code + "000000000"
            self.code = code

        super().save(*args, **kwargs)


class Part(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    count = models.IntegerField(null=True, blank=True)

    stored = models.ForeignKey(Stored, related_name= "stored", on_delete = models.SET_NULL, null=True, blank=True)

    ref = models.OneToOneField(Stored, on_delete = models.CASCADE, null=True, blank=True)

    tag = models.ManyToManyField(Tag, blank=True)

    code = models.CharField(max_length=16)

    def __str__(self):
        return self.template.name + " " + self.code


'''
class GeneratedCode(models.Model):
    code = models.CharField(max_length=100, default="", unique=True)
    generated_code = models.CharField(max_length=100, null=True)

    def save(self, *args, **kwargs):
        if not self.generated_code:
            self.generated_code = gen_code(self.code)
        
        super().save(*args, **kwargs)
'''
