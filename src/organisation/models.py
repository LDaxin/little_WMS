from datetime import timedelta

from django.db import models
from django.utils import timezone

from organisation.current import current_organisation_id
from organisation.permissions import PERMISSIONS


def _catalog_permissions():
    """The §3 catalogue as ``auth.Permission`` entries (area-prefixed codenames)."""
    entries = []
    for area, spec in PERMISSIONS.items():
        for scope in spec["scopes"]:
            for action in spec["actions"]:
                entries.append((
                    "%s_%s_%s" % (area, action, scope),
                    "%s: %s (%s)" % (area, action, scope),
                ))
    return entries


class PermissionArea(models.Model):
    """Hosts the permission catalogue in Django's ``auth.Permission`` (§3).

    The areas are logical (``article``, ``storage``, ``occasion``, …) and not all
    of them have a model yet, so every permission lives on this one content type
    with an area-prefixed codename (``article_view_all``).
    """

    class Meta:
        permissions = _catalog_permissions()


class Organisation(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Audit log retention (§32): empty = keep forever, otherwise days to keep.
    log_retention_days = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Delete audit log entries older than this many days. Empty = keep forever.",
    )

    def retention_cutoff(self):
        """Datetime before which audit entries should be purged, or None (forever)."""
        if not self.log_retention_days:
            return None
        return timezone.now() - timedelta(days=self.log_retention_days)

    def __str__(self):
        return self.name


class Role(models.Model):
    """A named collection of permissions, per organisation (§3).

    ``permissions`` links to Django's ``auth.Permission`` entries from the
    catalogue (see ``PermissionArea``).
    """

    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="roles", default=current_organisation_id)
    name = models.CharField(max_length=50)
    is_template = models.BooleanField(default=False)
    permissions = models.ManyToManyField("auth.Permission", blank=True, related_name="roles")

    class Meta:
        # templates and real roles may share a name (KI-020)
        unique_together = ("organisation", "name", "is_template")

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """A user's membership in one organisation, with their role there (§3, §22).

    A user can belong to several organisations — one profile per organisation.
    """

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="profiles")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, default=current_organisation_id)

    class Meta:
        unique_together = ("user", "organisation")

    def __str__(self):
        return "%s (%s)" % (self.user, self.role or "no role")
