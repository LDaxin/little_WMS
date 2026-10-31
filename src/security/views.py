"""Security hardening (§29)."""
import logging

from django.contrib.auth import authenticate, login
from django.core.cache import cache
from django.shortcuts import redirect, render

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
