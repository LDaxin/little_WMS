"""Notification center (§6) and notification rules."""
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from notifications.models import Notification, NotificationRule
from organisation.decorators import require_perm
from organisation.services import active_organisation


class FormNotificationRule(forms.ModelForm):
    class Meta:
        model = NotificationRule
        fields = [
            "trigger_type", "active", "threshold_days",
            "notify_roles", "notify_users", "channel_in_app", "channel_email",
            "channel_webhook", "webhook_secret",
        ]

    def __init__(self, *args, organisation=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organisation is not None:
            self.fields["notify_roles"].queryset = organisation.roles.filter(is_template=False)
            self.fields["notify_users"].queryset = User.objects.filter(
                profiles__organisation=organisation
            ).distinct()


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


@login_required(login_url='/accounts/login/')
@require_perm("notification.manage_rules_all")
def rules(request):
    organisation = active_organisation(request)
    return render(request, "notifications/rules.html", {
        "rules": NotificationRule.objects.filter(organisation=organisation),
    })


@login_required(login_url='/accounts/login/')
@require_perm("notification.manage_rules_all")
def ruleAdd(request):
    organisation = active_organisation(request)
    if request.method == "POST":
        form = FormNotificationRule(request.POST, organisation=organisation)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.organisation = organisation
            rule.save()
            form.save_m2m()
            return redirect("notification rules")
    else:
        form = FormNotificationRule(organisation=organisation)
    return render(request, "notifications/ruleForm.html", {"form": form})


@login_required(login_url='/accounts/login/')
@require_perm("notification.manage_rules_all")
def ruleEdit(request, ruleId):
    organisation = active_organisation(request)
    rule = get_object_or_404(NotificationRule, pk=ruleId, organisation=organisation)
    if request.method == "POST":
        form = FormNotificationRule(request.POST, instance=rule, organisation=organisation)
        if form.is_valid():
            form.save()
            return redirect("notification rules")
    else:
        form = FormNotificationRule(instance=rule, organisation=organisation)
    return render(request, "notifications/ruleForm.html", {"form": form})


@login_required(login_url='/accounts/login/')
@require_perm("notification.manage_rules_all")
def ruleDelete(request, ruleId):
    organisation = active_organisation(request)
    rule = get_object_or_404(NotificationRule, pk=ruleId, organisation=organisation)
    if request.method == "POST":
        rule.delete()
    return redirect("notification rules")
