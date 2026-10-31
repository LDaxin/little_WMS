"""Email verification (double opt-in, §30).

A user's address is only considered verified once they open the confirmation
link. The central mail service refuses to send to unverified addresses.
"""
import secrets

from django.urls import reverse

from hub.mail import send
from organisation.models import EmailVerification


def request_verification(user, request=None):
    """Create/refresh the user's verification record and send the link."""
    if not user.email:
        return None
    record, _ = EmailVerification.objects.get_or_create(user=user)
    record.email = user.email
    record.verified = False
    record.token = secrets.token_urlsafe(32)
    record.save()
    link = reverse("verify email", args=[record.token])
    if request is not None:
        link = request.build_absolute_uri(link)
    send(user.email, "Confirm your email address",
         "Please confirm your email address for little_WMS:\n\n%s\n" % link,
         require_verified=False)
    return record


def verify(token):
    """Mark the address verified for the given token. Returns the record or None."""
    record = EmailVerification.objects.filter(token=token).first()
    if record:
        record.verified = True
        record.save()
    return record


def is_verified(email):
    """Whether a verified record exists for this address."""
    return EmailVerification.objects.filter(email=email, verified=True).exists()


def is_user_verified(user):
    """Whether this user's address is verified."""
    return EmailVerification.objects.filter(user=user, verified=True).exists()
