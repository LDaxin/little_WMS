"""Managers that scope queries to the active organisation (§22)."""
from django.db import models

from organisation.current import get_current_organisation
from softdelete.models import SoftDeleteManager


class OrganisationFilterMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        organisation = get_current_organisation()
        if organisation is not None:
            qs = qs.filter(organisation=organisation)
        return qs


class OrganisationManager(OrganisationFilterMixin, models.Manager):
    """For org-scoped models without soft-delete."""


class SoftDeleteOrganisationManager(OrganisationFilterMixin, SoftDeleteManager):
    """For org-scoped models that also soft-delete."""
