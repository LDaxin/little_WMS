"""Notification center (§6)."""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from notifications.models import Notification
from organisation.decorators import require_perm


@login_required(login_url='/accounts/login/')
@require_perm("notification.view_all")
def notifications(request):
    return render(request, "notifications/notifications.html", {
        "notifications": request.user.notifications.all(),
    })


@login_required(login_url='/accounts/login/')
@require_perm("notification.view_all")
def notificationRead(request, notificationId):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')
    notification = get_object_or_404(Notification, pk=notificationId, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect("notifications")


@login_required(login_url='/accounts/login/')
@require_perm("notification.view_all")
def notificationsReadAll(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect("notifications")
