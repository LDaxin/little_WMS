from django.db import models
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from hub.fields import SelfForeignKey
from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager

# Create your models here.


class Location(SoftDeleteObject, models.Model):
    objects = SoftDeleteOrganisationManager()
    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)

    # Address – free-form lines for the variable part, optional structured
    # fields for filtering/sorting. Works for international formats (§28).
    line1 = models.CharField(max_length=200, blank=True)
    line2 = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=2, blank=True)  # ISO 3166-1 alpha-2

    # Coordinates (for the map, §15)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plus_code = models.CharField(max_length=20, blank=True)  # Open Location Code

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "l0"
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self):
        parts = [
            self.line1,
            self.line2,
            " ".join(p for p in [self.postal_code, self.city] if p),
            self.state,
            self.country,
        ]
        return ", ".join(p for p in parts if p)
