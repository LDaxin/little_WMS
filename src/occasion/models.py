from django.db import models
from softdelete.models import SoftDeleteObject

from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager


class CalendarEntry(SoftDeleteObject, models.Model):
    """A dated entry on the calendar (§2). Occasions are one entry type."""

    ENTRY_TYPE_CHOICES = [
        ("occasion", "Occasion"),
        ("maintenance", "Maintenance"),
        ("purchase", "Purchase"),
        ("disposal", "Disposal"),
        ("inventory", "Inventory"),
        ("other", "Other"),
    ]

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPE_CHOICES, default="occasion")
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    responsible_user = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["start_date", "id"]

    def __str__(self):
        return self.title


class OccasionType(SoftDeleteObject, models.Model):
    """Configurable occasion type (like article types), §2."""

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20, blank=True)
    custom_fields_schema = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class Occasion(SoftDeleteObject, models.Model):
    """The reason material is needed, backed by a calendar entry (§2)."""

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    calendar_entry = models.OneToOneField(CalendarEntry, on_delete=models.CASCADE, related_name="occasion")
    occasion_type = models.ForeignKey(OccasionType, on_delete=models.CASCADE)
    location = models.ForeignKey("location.Location", null=True, blank=True, on_delete=models.SET_NULL)
    participant_count = models.IntegerField(null=True, blank=True)
    attributes = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.calendar_entry.title


class Packlist(models.Model):
    """An article needed for an occasion, with a quantity and status (§2)."""

    STATUS_CHOICES = [
        ("needed", "Needed"),
        ("reserved", "Reserved"),
        ("checked_out", "Checked out"),
        ("returned", "Returned"),
    ]

    occasion = models.ForeignKey(Occasion, on_delete=models.CASCADE, related_name="packlist")
    article = models.ForeignKey("article.Article", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="needed")

    def __str__(self):
        return "%s x%s" % (self.article, self.quantity)
