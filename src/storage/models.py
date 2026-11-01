from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators
from hub import models as hub_models
from hub.fields import SelfForeignKey
from hub.models import BaseImage
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from django import forms
from space.models import Space
from tag.models import Tag
from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager
# Create your models here.



class StorageType(SoftDeleteObject, models.Model):
    objects = SoftDeleteOrganisationManager()
    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    name = models.CharField(_("Name"), max_length=200)
    symbol = models.CharField(_("Symbol"), max_length=20)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "st" 
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.name

class Storage(SoftDeleteObject, models.Model):
    objects = SoftDeleteOrganisationManager()
    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    name = models.CharField(_("Name"), max_length=200)
    typ = models.ForeignKey(StorageType, on_delete=models.CASCADE, verbose_name=_("Type"))
    parent = SelfForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Parent"))

    space = models.OneToOneField(Space,on_delete = models.CASCADE, related_name = "itemStorage", editable = False, blank = True, null = True)

    location = models.ForeignKey("location.Location", on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Location"))

    tags = models.ManyToManyField(Tag, blank=True, related_name="storages")

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = True, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "s0" 
            self.code = uCode
            uCode.save()
        if not self.space:
            space = Space()
            space.prefix = "s0"
            space.organisation_id = self.organisation_id or current_organisation_id()
            self.space = space
            space.save()
        super().save(*args, **kwargs)
    
    def __str__(self, *args, **kwargs):
        if self.parent != None:
            name = str(self.parent) + " / " + self.name
        else:
            name = self.name
        return name

    @property
    def primary_image(self):
        images = list(self.images.all())
        for image in images:
            if image.is_primary:
                return image
        return images[0] if images else None


class StorageImage(BaseImage):
    """An image of a storage (§15)."""

    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name="images")

    class Meta:
        ordering = ["order", "id"]


class FloorPlan(models.Model):
    """A floor plan for a storage (§15).

    The image is uploaded (Stage 1); the areas are drawn on it (Stage 2).
    """

    storage = models.OneToOneField(Storage, on_delete=models.CASCADE, related_name="floor_plan")
    name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="floorplans/%Y/%m/", null=True, blank=True)

    def __str__(self):
        return self.name or str(self.storage)


class FloorPlanArea(models.Model):
    """A rectangular area on a floor plan, optionally linked to a storage (§15).

    ``shape`` holds relative coordinates (0–1): ``{"x", "y", "w", "h"}``.
    """

    floor_plan = models.ForeignKey(FloorPlan, on_delete=models.CASCADE, related_name="areas")
    storage = models.ForeignKey(
        Storage, null=True, blank=True, on_delete=models.SET_NULL, related_name="plan_areas"
    )
    shape = models.JSONField(default=dict)
    label = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=7, default="#0d6efd")

    def __str__(self):
        return self.label or str(self.storage or "area")
        
