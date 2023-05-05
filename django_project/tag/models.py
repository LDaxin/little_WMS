from django.db import models
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from hub.fields import SelfForeignKey

# Create your models here.


class Tag(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=20)
    parent = SelfForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            self.code = "t0" + uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        if self.parent != None:
            return str(self.parent) + "/" + self.name
        else:
            return self.name
