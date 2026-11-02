from datetime import timedelta

from django.db import models
from django.utils import timezone

from hub.models import TokenisedModel
from organisation.current import current_organisation_id
from organisation.permissions import PERMISSIONS

# Sidebar navigation settings (§12).
SIDEBAR_POSITION_CHOICES = [("left", "Left"), ("right", "Right")]
VIEW_MODE_CHOICES = [("auto", "Auto"), ("mobile", "Always mobile"), ("desktop", "Always desktop")]


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
    # Preferred UI language (§14); empty = the server default.
    language = models.CharField(max_length=10, blank=True)
    # Sidebar navigation (§12), separate for desktop and mobile.
    sidebar_position_desktop = models.CharField(
        max_length=10, choices=SIDEBAR_POSITION_CHOICES, default="left"
    )
    sidebar_position_mobile = models.CharField(
        max_length=10, choices=SIDEBAR_POSITION_CHOICES, default="left"
    )
    icon_size_desktop = models.IntegerField(default=28)
    icon_size_mobile = models.IntegerField(default=28)
    text_size_desktop = models.IntegerField(default=16)
    text_size_mobile = models.IntegerField(default=16)
    view_mode = models.CharField(max_length=10, choices=VIEW_MODE_CHOICES, default="auto")
    # Scan feedback (§11): sound and vibration on the movement page.
    sound_enabled = models.BooleanField(default=True)
    vibration_enabled = models.BooleanField(default=True)
    volume = models.IntegerField(default=50)

    class Meta:
        unique_together = ("user", "organisation")

    def __str__(self):
        return "%s (%s)" % (self.user, self.role or "no role")


class Invitation(TokenisedModel):
    """An invitation to join an organisation with a pre-set role (§23).

    Link-based: the token is shareable; accepting creates a membership.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("expired", "Expired"),
        ("revoked", "Revoked"),
    ]

    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="invitations")
    email = models.EmailField(blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    invited_by = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def is_valid(self):
        """A pending invitation that has not expired."""
        return self.status == "pending" and not self.is_expired()

    def __str__(self):
        return "Invitation to %s" % self.organisation


class OrganisationRequest(models.Model):
    """A request to create a new organisation (§23).

    Used when the server registration policy is "request"; a server admin
    approves or rejects it.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    invitation = models.ForeignKey(Invitation, null=True, blank=True, on_delete=models.SET_NULL, related_name="requests")

    def __str__(self):
        return self.name


class EmailVerification(TokenisedModel):
    """A user's email confirmation state (double opt-in, §30).

    One record per user; a new token is issued on every request.
    """

    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name="email_verification")
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s (%s)" % (self.email, "verified" if self.verified else "unverified")

