"""Roles & Permissions UI (§3), organisation selection (§22) and invitations (§23)."""
from datetime import timedelta

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from organisation.decorators import require_perm
from organisation.models import Invitation, Organisation, OrganisationRequest, Role, UserProfile
from organisation.permissions import PERMISSIONS, ensure_role_templates
from organisation.services import active_organisation, set_active_organisation


# Standard types from §8.
DEFAULT_ARTICLE_TYPES = [
    ("tent", "TZ", True),
    ("kitchen", "KU", False),
    ("tool", "WZ", False),
    ("office", "BU", False),
    ("sport", "SP", False),
    ("tech", "TE", False),
    ("box", "KI", True),
    ("consumable", "VB", False),
    ("other", "SO", False),
]
DEFAULT_STORAGE_TYPES = [
    ("building", "GE"),
    ("room", "RA"),
    ("shelf", "RE"),
    ("compartment", "FA"),
    ("cabinet", "SC"),
    ("container", "CO"),
    ("vehicle", "FZ"),
]


def _organisation(request):
    """The active organisation of the request (§22)."""
    return active_organisation(request)


def _matrix(role):
    """Flat rows for the checkbox matrix (area × scope × action)."""
    granted = set(role.permissions.values_list("codename", flat=True)) if role else set()
    rows = []
    for obj, spec in PERMISSIONS.items():
        for scope in spec["scopes"]:
            for action in spec["actions"]:
                perm = "%s_%s" % (action, scope)
                codename = "%s_%s" % (obj, perm)
                rows.append({
                    "obj": obj,
                    "scope": scope,
                    "action": action,
                    "codename": codename,
                    "checked": codename in granted,
                })
    return rows


@login_required(login_url='/accounts/login/')
@require_perm("user.edit_role_all")
def roles(request, error=""):
    organisation = _organisation(request)
    roles = organisation.roles.filter(is_template=False)
    return render(request, "organisation/roles.html", {
        "templates": organisation.roles.filter(is_template=True),
        "roles": roles,
        "role_names": set(roles.values_list("name", flat=True)),
        "error": error,
    })


@login_required(login_url='/accounts/login/')
@require_perm("user.edit_role_all")
def roleCreate(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    organisation = _organisation(request)
    template = get_object_or_404(
        Role, organisation=organisation, name=request.POST.get("template", ""), is_template=True
    )
    name = request.POST.get("name", "").strip() or template.name
    if Role.objects.filter(organisation=organisation, name=name, is_template=False).exists():
        return roles(request, error="A role named '%s' already exists." % name)
    role = Role.objects.create(organisation=organisation, name=name, is_template=False)
    role.permissions.set(template.permissions.all())
    return redirect("roles")


@login_required(login_url='/accounts/login/')
@require_perm("user.edit_role_all")
def roleDetail(request, roleId):
    organisation = _organisation(request)
    role = get_object_or_404(Role, pk=roleId, organisation=organisation)
    return render(request, "organisation/roleForm.html", {"role": role, "rows": _matrix(role)})


@login_required(login_url='/accounts/login/')
@require_perm("user.edit_role_all")
def roleSave(request, roleId):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    organisation = _organisation(request)
    role = get_object_or_404(Role, pk=roleId, organisation=organisation)
    role.permissions.set(Permission.objects.filter(codename__in=request.POST.getlist("perm")))
    return redirect("role detail", roleId=role.pk)


@login_required(login_url='/accounts/login/')
@require_perm("user.edit_role_all")
def roleDelete(request, roleId):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    organisation = _organisation(request)
    role = get_object_or_404(Role, pk=roleId, organisation=organisation, is_template=False)
    role.delete()
    return redirect("roles")


@login_required(login_url='/accounts/login/')
@require_perm("user.view_all")
def users(request):
    organisation = _organisation(request)
    rows = [
        {"user": p.user, "profile": p}
        for p in UserProfile.objects.filter(organisation=organisation).select_related("user")
    ]
    return render(request, "organisation/users.html", {
        "rows": rows,
        "roles": organisation.roles.filter(is_template=False),
        "invitations": organisation.invitations.filter(status="pending"),
    })


@login_required(login_url='/accounts/login/')
@require_perm("user.edit_role_all")
def userRole(request, userId):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    organisation = _organisation(request)
    user = get_object_or_404(User, pk=userId)
    role_id = request.POST.get("role") or None
    role = organisation.roles.filter(pk=role_id).first() if role_id else None
    profile, _ = UserProfile.objects.get_or_create(user=user, organisation=organisation)
    profile.role = role
    profile.save()
    return redirect("users")


@login_required(login_url='/accounts/login/')
def selectOrganisation(request):
    """Pick the active organisation after login (§22)."""
    profiles = request.user.profiles.select_related("organisation")
    if profiles.count() == 1:
        set_active_organisation(request, profiles.first().organisation)
        return redirect("hub")
    if not profiles.exists():
        profile = UserProfile.objects.create(user=request.user, organisation_id=1)
        set_active_organisation(request, profile.organisation)
        return redirect("hub")
    return render(request, "organisation/selectOrganisation.html", {"profiles": profiles})


@login_required(login_url='/accounts/login/')
def switchOrganisation(request):
    """Switch the active organisation (§22)."""
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    organisation = get_object_or_404(Organisation, pk=request.POST.get("organisation"))
    if not request.user.is_superuser and not request.user.profiles.filter(
        organisation=organisation
    ).exists():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    set_active_organisation(request, organisation)
    return redirect(request.POST.get("next") or "hub")


def _accept_invitation(invitation, user):
    """Create the membership for ``user`` and mark the invitation accepted."""
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        organisation=invitation.organisation,
        defaults={"role": invitation.role},
    )
    if not created and profile.role is None:
        profile.role = invitation.role
        profile.save()
    invitation.status = "accepted"
    invitation.accepted_at = timezone.now()
    invitation.save()


@login_required(login_url='/accounts/login/')
@require_perm("user.invite_all")
def inviteCreate(request):
    """Create an invitation link for the active organisation (§23)."""
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    organisation = _organisation(request)
    role_id = request.POST.get("role") or None
    role = organisation.roles.filter(pk=role_id).first() if role_id else None
    days = request.POST.get("days", "").strip()
    expires_at = timezone.now() + timedelta(days=int(days)) if days.isdigit() else None
    Invitation.objects.create(
        organisation=organisation,
        email=request.POST.get("email", "").strip(),
        role=role,
        invited_by=request.user,
        expires_at=expires_at,
    )
    return redirect("users")


@login_required(login_url='/accounts/login/')
@require_perm("user.invite_all")
def inviteRevoke(request, invitationId):
    """Revoke a pending invitation (§23)."""
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    organisation = _organisation(request)
    invitation = get_object_or_404(Invitation, pk=invitationId, organisation=organisation)
    invitation.status = "revoked"
    invitation.save()
    return redirect("users")


def inviteAccept(request, token):
    """Public accept page: register or log in, then join the organisation (§23)."""
    invitation = get_object_or_404(Invitation, token=token)
    if not invitation.is_valid():
        return render(request, "organisation/inviteInvalid.html", {"invitation": invitation})

    if request.user.is_authenticated:
        _accept_invitation(invitation, request.user)
        set_active_organisation(request, invitation.organisation)
        return redirect("hub")

    error = ""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")
        if not username or not email or not password:
            error = "Username, email, and password are required."
        elif password != password2:
            error = "The passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "That username is already taken."
        else:
            user = User.objects.create_user(username, email, password)
            login(request, user)
            _accept_invitation(invitation, user)
            set_active_organisation(request, invitation.organisation)
            return redirect("hub")
    return render(request, "organisation/inviteAccept.html",
                  {"invitation": invitation, "error": error})


def _registration_policy():
    from hub.models import Settings

    settings = Settings.objects.first()
    return settings.registration_policy if settings else "invite"


def _unique_slug(name):
    from django.utils.text import slugify

    base = slugify(name) or "org"
    slug = base
    n = 1
    while Organisation.objects.filter(slug=slug).exists():
        n += 1
        slug = "%s-%s" % (base, n)
    return slug


def _create_organisation(name):
    """Create an organisation with a role holding every permission (§23)."""
    from organisation.permissions import all_codenames

    organisation = Organisation.objects.create(name=name, slug=_unique_slug(name))
    role = Role.objects.create(organisation=organisation, name="Admin")
    role.permissions.set(Permission.objects.filter(codename__in=all_codenames()))
    return organisation


def registerOrganisation(request):
    """Public registration page, following the server policy (§23)."""
    policy = _registration_policy()
    error = ""
    if policy == "open" and request.method == "POST":
        name = request.POST.get("name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        if not name or not username or not email or not password:
            error = "All fields are required."
        elif User.objects.filter(username=username).exists():
            error = "That username is already taken."
        else:
            organisation = _create_organisation(name)
            user = User.objects.create_user(username, email, password)
            UserProfile.objects.create(
                user=user, organisation=organisation, role=organisation.roles.get(name="Admin")
            )
            login(request, user)
            set_active_organisation(request, organisation)
            return redirect("hub")
    elif policy == "request" and request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        reason = request.POST.get("reason", "").strip()
        if not name or not email or not reason:
            error = "Name, email, and reason are required."
        else:
            OrganisationRequest.objects.create(name=name, email=email, reason=reason)
            return render(request, "organisation/registerRequested.html", {"name": name})
    return render(request, "organisation/register.html", {"policy": policy, "error": error})


@login_required(login_url='/accounts/login/')
def organisationRequests(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    return render(request, "organisation/organisationRequests.html", {
        "requests": OrganisationRequest.objects.all(),
    })


@login_required(login_url='/accounts/login/')
def organisationRequestReview(request, requestId):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    organisation_request = get_object_or_404(OrganisationRequest, pk=requestId)
    action = request.POST.get("action")
    if action == "approve":
        organisation = _create_organisation(organisation_request.name)
        organisation_request.invitation = Invitation.objects.create(
            organisation=organisation,
            email=organisation_request.email,
            role=organisation.roles.get(name="Admin"),
            invited_by=request.user,
        )
        organisation_request.status = "approved"
    elif action == "reject":
        organisation_request.status = "rejected"
    organisation_request.reviewed_by = request.user
    organisation_request.reviewed_at = timezone.now()
    organisation_request.save()
    return redirect("organisation requests")


@login_required(login_url='/accounts/login/')
def serverSettings(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    from hub.models import Settings

    settings = Settings.objects.first() or Settings.objects.create()
    if request.method == "POST":
        policy = request.POST.get("registration_policy")
        if policy in dict(Settings.REGISTRATION_POLICY_CHOICES):
            settings.registration_policy = policy
            settings.save()
        return redirect("server settings")
    return render(request, "organisation/serverSettings.html", {
        "settings": settings,
        "policies": Settings.REGISTRATION_POLICY_CHOICES,
    })


def _load_defaults():
    """Create the standard article and storage types from §8."""
    from article.models import ArticleType
    from storage.models import StorageType

    for name, symbol, toggle in DEFAULT_ARTICLE_TYPES:
        ArticleType.objects.get_or_create(
            name=name, defaults={"symbol": symbol, "article_toggle_space": toggle}
        )
    for name, symbol in DEFAULT_STORAGE_TYPES:
        StorageType.objects.get_or_create(name=name, defaults={"symbol": symbol})


@login_required(login_url='/accounts/login/')
@require_perm("settings.edit_all")
def configuration(request):
    """Organisation configuration: article types, storage types, role templates (§8)."""
    from article.models import ArticleType
    from storage.models import StorageType

    organisation = _organisation(request)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "article_type":
            name = request.POST.get("name", "").strip()
            if name:
                ArticleType.objects.create(
                    name=name,
                    symbol=request.POST.get("symbol", "").strip(),
                    article_toggle_space=request.POST.get("article_toggle_space") == "on",
                )
        elif action == "storage_type":
            name = request.POST.get("name", "").strip()
            if name:
                StorageType.objects.create(
                    name=name, symbol=request.POST.get("symbol", "").strip()
                )
        elif action == "load_defaults":
            _load_defaults()
        elif action == "role_templates":
            ensure_role_templates(organisation)
        return redirect("configuration")
    return render(request, "organisation/configuration.html", {
        "article_types": ArticleType.objects.all(),
        "storage_types": StorageType.objects.all(),
    })
