"""Security hardening (§29) and GDPR (§35)."""
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from organisation.decorators import require_perm

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 900


def _key(kind, value):
    return "login_fail_%s_%s" % (kind, value)


def _is_locked(kind, value):
    return cache.get(_key(kind, value), 0) >= MAX_ATTEMPTS


def _record_failure(kind, value):
    key = _key(kind, value)
    cache.set(key, cache.get(key, 0) + 1, LOCKOUT_SECONDS)


def loginView(request):
    """Login with rate limiting per IP and per account (§29)."""
    error = ""
    if request.method == "POST":
        ip = request.META.get("REMOTE_ADDR", "")
        username = request.POST.get("username", "")
        if _is_locked("ip", ip) or _is_locked("user", username):
            error = "Too many failed attempts. Try again later."
            logger.warning("Login locked out for ip=%s user=%s", ip, username)
        else:
            user = authenticate(
                request, username=username, password=request.POST.get("password", "")
            )
            if user is not None:
                login(request, user)
                return redirect(request.GET.get("next") or "hub")
            _record_failure("ip", ip)
            _record_failure("user", username)
            error = "Invalid username or password."
            logger.warning("Failed login for ip=%s user=%s", ip, username)
    return render(request, "registration/login.html", {"error": error})


@login_required(login_url='/accounts/login/')
def myData(request):
    """Export the user's personal data (§35)."""
    from audit.models import AuditLog
    from loans.models import Loan

    user = request.user
    organisations = list(user.profiles.values_list("organisation", flat=True))
    data = {
        "username": user.username,
        "email": user.email,
        "profile": [
            {"organisation": p.organisation.name, "role": p.role.name if p.role else None}
            for p in user.profiles.select_related("organisation", "role")
        ],
        "activities": [
            {"action": a.action, "timestamp": a.timestamp.isoformat(), "object": str(a.content_object)}
            for a in AuditLog.objects.filter(user=user)
        ],
        "loans": [
            {
                "article": str(loan.article),
                "lender": loan.lender_name or str(loan.lender_organisation),
                "start": loan.start_date.isoformat(),
                "status": loan.status,
            }
            for loan in Loan.objects.filter(borrower_organisation__in=organisations)
        ],
    }
    response = JsonResponse(data)
    response["Content-Disposition"] = 'attachment; filename="my-data.json"'
    return response


@login_required(login_url='/accounts/login/')
@require_perm("user.deactivate_all")
def deleteUser(request, userId):
    """Delete a user, anonymising their audit-log entries (§35)."""
    from django.contrib.auth.models import User

    from audit.models import AuditLog

    user = get_object_or_404(User, pk=userId)
    if request.method == "POST":
        AuditLog.objects.filter(user=user).update(user=None)
        user.delete()
    return redirect("users")
