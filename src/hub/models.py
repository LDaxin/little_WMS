from django.db import models
from django.utils.translation import gettext_lazy as _
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from hub.fields import SelfForeignKey

# Create your models here.
class Settings(SoftDeleteObject, models.Model):
    REGISTRATION_POLICY_CHOICES = [
        ("open", _("Open")),
        ("invite", _("Invite only")),
        ("request", _("Request")),
    ]

    storageDepth = models.IntegerField(default = 7)
    registration_policy = models.CharField(
        max_length=10, choices=REGISTRATION_POLICY_CHOICES, default="invite"
    )
    onboarding_completed = models.BooleanField(default=False)


class EmailPreference(models.Model):
    """A user's per-category email opt-out (§6).

    A missing row means subscribed, so the default is opt-out and new categories
    need no data migration.
    """

    CATEGORY_CHOICES = [
        ("notifications", _("Notifications")),
        ("invitations", _("Invitations")),
    ]

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="email_preferences")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    subscribed = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "category")

    def __str__(self):
        return "%s: %s" % (self.category, "subscribed" if self.subscribed else "unsubscribed")


class BaseImage(models.Model):
    """An image attached to an object (§15).

    Concrete subclasses add the owner foreign key. On save the image is scaled
    to ``MAX_EDGE`` and a thumbnail is generated with Pillow (already required
    by ``ImageField``).
    """

    MAX_EDGE = 1600
    THUMB_EDGE = 300

    image = models.ImageField(upload_to="images/%Y/%m/")
    thumbnail = models.ImageField(upload_to="images/thumbs/%Y/%m/", blank=True)
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.image and not self.thumbnail:
            self._process()
        super().save(*args, **kwargs)

    def _process(self):
        from io import BytesIO

        from django.core.files.base import ContentFile
        from PIL import Image, ImageOps

        self.image.open()
        img = ImageOps.exif_transpose(Image.open(self.image)).convert("RGB")
        name = self.image.name

        img.thumbnail((self.MAX_EDGE, self.MAX_EDGE))
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85)
        self.image.save(name, ContentFile(buf.getvalue()), save=False)

        thumb = img.copy()
        thumb.thumbnail((self.THUMB_EDGE, self.THUMB_EDGE))
        tbuf = BytesIO()
        thumb.save(tbuf, format="JPEG", quality=85)
        self.thumbnail.save(name, ContentFile(tbuf.getvalue()), save=False)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        self.thumbnail.delete(save=False)
        super().delete(*args, **kwargs)

