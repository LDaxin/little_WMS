from django.db import models
from softdelete.models import SoftDeleteObject

from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager


class Lending(SoftDeleteObject, models.Model):
    """An article lent to an external person (§20).

    The article stays the organisation's property; the lending records who has
    it and until when. The period is a ``loan`` calendar entry.
    """

    STATUS_CHOICES = [
        ("active", "Active"),
        ("returned", "Returned"),
    ]

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    article = models.ForeignKey("article.Article", on_delete=models.CASCADE, related_name="lendings")
    calendar_entry = models.OneToOneField("planning.CalendarEntry", on_delete=models.CASCADE, related_name="lending")
    borrower_name = models.CharField(max_length=200)
    borrower_email = models.EmailField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    occasion = models.ForeignKey("occasion.Occasion", null=True, blank=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True)

    def __str__(self):
        return "%s -> %s" % (self.article, self.borrower_name)


class Loan(SoftDeleteObject, models.Model):
    """The organisation borrows an article from an external lender (§20).

    The article is marked ``borrowed`` (not the organisation's property).
    """

    LENDER_TYPE_CHOICES = [
        ("person", "External person"),
        ("organisation", "Another organisation"),
    ]
    STATUS_CHOICES = [
        ("active", "Active"),
        ("returned", "Returned"),
    ]

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    article = models.ForeignKey("article.Article", on_delete=models.CASCADE, related_name="loans")
    lender_type = models.CharField(max_length=20, choices=LENDER_TYPE_CHOICES, default="person")
    lender_name = models.CharField(max_length=200, blank=True)
    lender_organisation = models.ForeignKey("organisation.Organisation", null=True, blank=True, on_delete=models.SET_NULL, related_name="loans_out")
    borrower_organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, related_name="loans_in", default=current_organisation_id)
    occasion = models.ForeignKey("occasion.Occasion", null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    notes = models.TextField(blank=True)

    def __str__(self):
        return "%s from %s" % (self.article, self.lender_name or self.lender_organisation)
