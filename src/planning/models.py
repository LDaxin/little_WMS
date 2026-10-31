from django.db import models
from softdelete.models import SoftDeleteObject

from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager


class RecurrenceRule(SoftDeleteObject, models.Model):
    """How a calendar entry repeats (§2)."""

    FREQUENCY_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    interval = models.IntegerField(default=1)
    end_date = models.DateField(null=True, blank=True)
    end_after_occurrences = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "every %s %s" % (self.interval, self.frequency)


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
    recurrence_rule = models.ForeignKey(RecurrenceRule, null=True, blank=True, on_delete=models.SET_NULL, related_name="entries")
    article = models.ForeignKey("article.Article", null=True, blank=True, on_delete=models.CASCADE, related_name="calendar_entries")

    class Meta:
        ordering = ["start_date", "id"]

    def __str__(self):
        return self.title
