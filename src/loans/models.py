from django.db import models
from django.utils.translation import gettext_lazy as _
from softdelete.models import SoftDeleteObject

from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager


class Lending(SoftDeleteObject, models.Model):
    """An article lent to an external person (§20).

    The article stays the organisation's property; the lending records who has
    it and until when. The period is a ``loan`` calendar entry.
    """

    STATUS_CHOICES = [
        ("active", _("Active")),
        ("returned", _("Returned")),
    ]

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    article = models.ForeignKey("article.Article", on_delete=models.CASCADE, related_name="lendings")
    calendar_entry = models.OneToOneField("planning.CalendarEntry", on_delete=models.CASCADE, related_name="lending")
    borrower_name = models.CharField(_("Borrower"), max_length=200)
    borrower_email = models.EmailField(_("Borrower email"), blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    occasion = models.ForeignKey("occasion.Occasion", null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("Occasion"))
    notes = models.TextField(_("Notes"), blank=True)

    def __str__(self):
        return "%s -> %s" % (self.article, self.borrower_name)


class Loan(SoftDeleteObject, models.Model):
    """The organisation borrows an article from an external lender (§20).

    The article is marked ``borrowed`` (not the organisation's property).
    """

    LENDER_TYPE_CHOICES = [
        ("person", _("External person")),
        ("organisation", _("Another organisation")),
    ]
    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("active", _("Active")),
        ("returned", _("Returned")),
    ]

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    article = models.ForeignKey("article.Article", on_delete=models.CASCADE, related_name="loans")
    lender_type = models.CharField(_("Lender type"), max_length=20, choices=LENDER_TYPE_CHOICES, default="person")
    lender_name = models.CharField(_("Lender"), max_length=200, blank=True)
    lender_organisation = models.ForeignKey("organisation.Organisation", null=True, blank=True, on_delete=models.SET_NULL, related_name="loans_out")
    borrower_organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, related_name="loans_in", default=current_organisation_id)
    occasion = models.ForeignKey("occasion.Occasion", null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"), null=True, blank=True)
    status = models.CharField(_("Status"), max_length=10, choices=STATUS_CHOICES, default="active")
    notes = models.TextField(_("Notes"), blank=True)

    def __str__(self):
        return "%s from %s" % (self.article, self.lender_name or self.lender_organisation)


class OrganisationMembership(models.Model):
    """A pool membership: a pool organisation lends to a member (§20)."""

    pool = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, related_name="members")
    member = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, related_name="pools")
    can_borrow = models.BooleanField(default=True)
    can_add = models.BooleanField(default=False)

    def __str__(self):
        return "%s in pool %s" % (self.member, self.pool)
