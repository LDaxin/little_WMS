from django.db import models
from softdelete.models import SoftDeleteObject

from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager


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
    calendar_entry = models.OneToOneField("planning.CalendarEntry", on_delete=models.CASCADE, related_name="occasion")
    occasion_type = models.ForeignKey(OccasionType, on_delete=models.CASCADE)
    location = models.ForeignKey("location.Location", null=True, blank=True, on_delete=models.SET_NULL)
    participant_count = models.IntegerField(null=True, blank=True)
    attributes = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.calendar_entry.title


class OccasionTemplate(SoftDeleteObject, models.Model):
    """A reusable occasion with a default packlist (§2).

    `default_packlist` is a list of {"article": <pk>, "quantity": <int>}.
    """

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    name = models.CharField(max_length=100)
    occasion_type = models.ForeignKey(OccasionType, on_delete=models.CASCADE)
    default_packlist = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name


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
