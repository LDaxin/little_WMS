from django.db import models
from django.utils.translation import gettext_lazy as _
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from hub.fields import SelfForeignKey
from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager

# Create your models here.


class TagCategory(SoftDeleteObject, models.Model):
    objects = SoftDeleteOrganisationManager()
    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    name = models.CharField(_("Name"), max_length=50)
    color = models.CharField(_("Color"), max_length=7, default="#6c757d")
    allow_multiple = models.BooleanField(default=True)
    inherit_to_contents = models.BooleanField(default=False)

    def __str__(self, *args, **kwargs):
        return self.name


class Tag(SoftDeleteObject, models.Model):
    objects = SoftDeleteOrganisationManager()
    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    name = models.CharField(_("Name"), max_length=20)
    parent = SelfForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Parent"))
    category = models.ForeignKey(TagCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Category"))
    color = models.CharField(_("Color"), max_length=7, default="#6c757d")
    icon = models.CharField(_("Icon"), max_length=20, blank=True)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "t0"
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        if self.parent != None:
            return str(self.parent) + "/" + self.name
        else:
            return self.name
