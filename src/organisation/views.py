"""Roles & Permissions UI (§3)."""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from organisation.models import Organisation, Role, UserProfile
from organisation.permissions import PERMISSIONS


def _organisation(request):
    """The user's organisation, falling back to the default one (§3)."""
    profile = getattr(request.user, "profile", None)
    if profile is not None:
        return profile.organisation
    return Organisation.objects.get(pk=1)


def _matrix(role):
    """Flat rows for the checkbox matrix (object × scope × action)."""
    rows = []
    for obj, spec in PERMISSIONS.items():
        for scope in spec["scopes"]:
            for action in spec["actions"]:
                perm = "%s_%s" % (action, scope)
                rows.append({
                    "obj": obj,
                    "scope": scope,
                    "action": action,
                    "value": "%s.%s" % (obj, perm),
                    "checked": perm in (role.permissions.get(obj, []) if role else []),
                })
    return rows


def _group(perms):
    """Turn ["article.view_all", ...] into {"article": ["view_all"], ...}."""
    result = {}
    for perm in perms:
        obj, _, action = perm.partition(".")
        result.setdefault(obj, []).append(action)
    return result


@login_required(login_url='/accounts/login/')
def roles(request):
    organisation = _organisation(request)
    return render(request, "organisation/roles.html", {
        "templates": organisation.roles.filter(is_template=True),
        "roles": organisation.roles.filter(is_template=False),
    })


@login_required(login_url='/accounts/login/')
def roleCreate(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    organisation = _organisation(request)
    template = get_object_or_404(
        Role, organisation=organisation, name=request.POST.get("template", ""), is_template=True
    )
    name = request.POST.get("name", "").strip() or template.name
    Role.objects.create(
        organisation=organisation, name=name, is_template=False, permissions=template.permissions
    )
    return redirect("roles")


@login_required(login_url='/accounts/login/')
def roleDetail(request, roleId):
    organisation = _organisation(request)
    role = get_object_or_404(Role, pk=roleId, organisation=organisation)
    return render(request, "organisation/roleForm.html", {"role": role, "rows": _matrix(role)})


@login_required(login_url='/accounts/login/')
def roleSave(request, roleId):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    organisation = _organisation(request)
    role = get_object_or_404(Role, pk=roleId, organisation=organisation)
    role.permissions = _group(request.POST.getlist("perm"))
    role.save()
    return redirect("role detail", roleId=role.pk)


@login_required(login_url='/accounts/login/')
def roleDelete(request, roleId):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    organisation = _organisation(request)
    role = get_object_or_404(Role, pk=roleId, organisation=organisation, is_template=False)
    role.delete()
    return redirect("roles")


@login_required(login_url='/accounts/login/')
def users(request):
    organisation = _organisation(request)
    profiles = {p.user_id: p for p in UserProfile.objects.filter(organisation=organisation)}
    rows = [{"user": user, "profile": profiles.get(user.pk)} for user in User.objects.all()]
    return render(request, "organisation/users.html", {
        "rows": rows,
        "roles": organisation.roles.filter(is_template=False),
    })


@login_required(login_url='/accounts/login/')
def userRole(request, userId):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    organisation = _organisation(request)
    user = get_object_or_404(User, pk=userId)
    role_id = request.POST.get("role") or None
    role = organisation.roles.filter(pk=role_id).first() if role_id else None
    profile, _ = UserProfile.objects.get_or_create(user=user, defaults={"organisation": organisation})
    profile.role = role
    profile.organisation = organisation
    profile.save()
    return redirect("users")
