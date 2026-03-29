from django.db import models
import muid
from softdelete.models import SoftDeleteObject

# Create your models here.

class MuidCode(SoftDeleteObject, models.Model):
    muidCodePretty = models.CharField(max_length = 13, editable = False, unique = True)
    muidCodeHash = models.BinaryField(editable = False, unique = True)
    codeReadable = models.CharField(max_length = 16, editable = False, unique = True)
    code = models.CharField(max_length = 14, editable = False, unique = True, blank=True)
    prefix = models.CharField(max_length = 2, editable = False)
    used = models.BooleanField(default = True)

    def save(self, *args, **kwargs):
        if not self.code:
            while True:
                muidCodeHash = muid.create()
                muidCodePretty = muid.animal(muidCodeHash)
                print(muidCodePretty)
                if len(muidCodePretty) < 14:
                    break

            codeReadable = self.prefix + " " + muidCodePretty
            print(codeReadable)
            code = codeReadable.replace(" ", "")
            print(code)
            self.muidCodePretty = muidCodePretty
            self.muidCodeHash = muidCodeHash
            self.codeReadable = codeReadable
            self.code = code
        super().save(*args, **kwargs)
    
    def __str__(self, *args, **kwargs):
        return self.codeReadable

