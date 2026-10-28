"""Audit logging (§32).

Explicit calls at the choke points, not global signals — only the operations
that matter are logged, with the caller's ``user``.
"""
from django.contrib.contenttypes.models import ContentType


def log(action, obj, user=None, changes=None, session=None):
    """Write one audit entry for ``obj`` and return it."""
    from audit.models import AuditLog

    if user is not None and not getattr(user, "is_authenticated", False):
        user = None
    return AuditLog.objects.create(
        user=user,
        organisation_id=getattr(obj, "organisation_id", None) or 1,
        action=action,
        content_type=ContentType.objects.get_for_model(obj),
        object_id=obj.pk,
        changes=changes or {},
        session=session,
    )
