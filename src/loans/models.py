from django.db import models
from django.utils.translation import gettext_lazy as _
from softdelete.models import SoftDeleteObject

from hub.models import TokenisedModel
from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager


class Loan(SoftDeleteObject, models.Model):
    """An article moving to or from outside the organisation (§20).

    ``direction`` ``out``: the organisation lends an article to a borrower.
    ``direction`` ``in``: the organisation borrows an article from a lender.
    The period is a ``loan`` calendar entry, created with the loan.
    """

    DIRECTION_CHOICES = [
        ("out", _("Lent out")),
        ("in", _("Borrowed in")),
    ]
    PARTY_TYPE_CHOICES = [
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
    calendar_entry = models.OneToOneField("planning.CalendarEntry", on_delete=models.CASCADE, related_name="loan")
    direction = models.CharField(_("Direction"), max_length=3, choices=DIRECTION_CHOICES, default="out")
    party_type = models.CharField(_("Party type"), max_length=20, choices=PARTY_TYPE_CHOICES, default="person")
    party_name = models.CharField(_("Name"), max_length=200, blank=True)
    party_email = models.EmailField(_("Email"), blank=True)
    party_organisation = models.ForeignKey("organisation.Organisation", null=True, blank=True, on_delete=models.SET_NULL, related_name="loans")
    occasion = models.ForeignKey("occasion.Occasion", null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("Occasion"))
    status = models.CharField(_("Status"), max_length=10, choices=STATUS_CHOICES, default="active")
    notes = models.TextField(_("Notes"), blank=True)
    lend_link = models.ForeignKey("LendLink", null=True, blank=True, on_delete=models.SET_NULL, related_name="loans")

    def party_label(self):
        """The other party: a person's name or the organisation."""
        return self.party_name or (self.party_organisation.name if self.party_organisation else "")

    def __str__(self):
        arrow = "->" if self.direction == "out" else "<-"
        return "%s %s %s" % (self.article, arrow, self.party_label())


class OrganisationMembership(models.Model):
    """A pool membership: a pool organisation lends to a member (§20)."""

    pool = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, related_name="members")
    member = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, related_name="pools")
    can_borrow = models.BooleanField(default=True)
    can_add = models.BooleanField(default=False)

    def __str__(self):
        return "%s in pool %s" % (self.member, self.pool)


class LendLink(TokenisedModel):
    """A capability URL for an external person to lend items to the org (§20).

    The external person opens the link, enters their name and email once, and
    manages a list of items. The link stays valid until deactivated or expired.
    """

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    label = models.CharField(_("Label"), max_length=100, blank=True)
    lender_name = models.CharField(_("Lender"), max_length=200, blank=True)
    lender_email = models.EmailField(_("Lender email"), blank=True)
    is_active = models.BooleanField(default=True)
    password_hash = models.CharField(max_length=128, blank=True)
    created_by = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.is_active and not self.is_expired()

    def __str__(self):
        return self.label or "Lend link %s" % self.pk
