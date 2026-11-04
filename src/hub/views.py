from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from .models import *
import article.models as ar
#from storage.models import *
import storage.models as st
import location.models as lo
import tag.models as ta
import codeSystem.models as co
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from organisation.decorators import require_perm

# Create your views here.




@login_required(login_url='/accounts/login/')
def hub(request):
    return render(request, "hub/hub.html", context={"symbol":"Logo", "fields":['Movement', 'Article', 'Storage', "Code"], "paType":ar.ArticleType.objects.all(), "stType":st.StorageType.objects.all()})


def manifest(request):
    """Web app manifest (§34)."""
    return JsonResponse({
        "name": "little_WMS",
        "short_name": "little_WMS",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#0d6efd",
        "icons": [
            {"src": "/static/hub/symbols/Logo.svg", "sizes": "any", "type": "image/svg+xml"},
        ],
    })


def serviceWorker(request):
    """Service worker caching the app shell (§34)."""
    return render(request, "hub/sw.js", content_type="application/javascript")


@login_required(login_url='/accounts/login/')
def onboarding(request):
    """First-run setup wizard (§8)."""
    from article.models import ArticleType
    from hub.models import Settings
    from organisation.permissions import ensure_role_templates
    from organisation.services import active_organisation
    from organisation.views import DEFAULT_ARTICLE_TYPES, DEFAULT_STORAGE_TYPES
    from storage.models import StorageType

    settings = Settings.objects.first() or Settings.objects.create()
    if request.method == "POST":
        if not request.POST.get("skip"):
            for name, symbol, toggle in DEFAULT_ARTICLE_TYPES:
                if request.POST.get("article_%s" % name):
                    ArticleType.objects.get_or_create(
                        name=name, defaults={"symbol": symbol, "article_toggle_space": toggle}
                    )
            for name, symbol in DEFAULT_STORAGE_TYPES:
                if request.POST.get("storage_%s" % name):
                    StorageType.objects.get_or_create(name=name, defaults={"symbol": symbol})
            if request.POST.get("role_templates"):
                ensure_role_templates(active_organisation(request))
        settings.onboarding_completed = True
        settings.save()
        return redirect("hub")
    return render(request, "hub/onboarding.html", {
        "article_types": DEFAULT_ARTICLE_TYPES,
        "storage_types": DEFAULT_STORAGE_TYPES,
    })


@login_required(login_url='/accounts/login/')
def dashboard(request):
    """Command center with permission-gated widgets (§24)."""
    from datetime import date

    from article.models import Article
    from audit.models import AuditLog
    from notifications.checks import run_checks
    from occasion.models import Occasion
    from organisation.permissions import has_perm
    from organisation.services import active_organisation
    from storage.models import Storage

    organisation = active_organisation(request)
    context = {}

    if has_perm(request.user, "occasion.view_all", organisation):
        context["upcomingOccasions"] = Occasion.objects.filter(
            calendar_entry__start_date__gte=date.today()
        ).order_by("calendar_entry__start_date")[:5]

    if has_perm(request.user, "notification.view_all", organisation):
        context["dashboardNotifications"] = request.user.notifications.filter(is_read=False)[:5]

    if has_perm(request.user, "article.view_all", organisation):
        context["alerts"] = list(run_checks(organisation))[:10]
        context["recentActivity"] = AuditLog.objects.all()[:5]

    if has_perm(request.user, "settings.view_all", organisation):
        context["statistics"] = {
            "articles": Article.objects.count(),
            "storages": Storage.objects.count(),
            "occasions": Occasion.objects.count(),
        }

    if has_perm(request.user, "article.create_all", organisation) or has_perm(
        request.user, "article.move_all", organisation
    ):
        context["quickActions"] = True

    from querybuilder.services import ARTICLE_FIELDS, QueryError, parse
    from savedviews.models import SavedView

    widgets = []
    for view in SavedView.objects.filter(owner=request.user, show_on_dashboard=True):
        articles = Article.objects.all()
        try:
            articles = articles.filter(parse(view.query, ARTICLE_FIELDS))
        except QueryError:
            pass
        widgets.append({"view": view, "articles": articles[:5]})
    if widgets:
        context["viewWidgets"] = widgets

    return render(request, "hub/dashboard.html", context)


def _soft_delete_models():
    from django.apps import apps

    from softdelete.models import SoftDeleteObject

    return [m for m in apps.get_models() if issubclass(m, SoftDeleteObject)]


def _deleted_groups():
    """Soft-deleted objects of the active organisation, grouped by model (§27)."""
    from django.contrib.contenttypes.models import ContentType

    from organisation.current import get_current_organisation

    organisation = get_current_organisation()
    groups = []
    for model in _soft_delete_models():
        qs = model.objects.deleted_set()
        if any(f.name == "organisation" for f in model._meta.get_fields()):
            qs = qs.filter(organisation=organisation)
        objects = list(qs)
        if objects:
            ct_id = ContentType.objects.get_for_model(model).pk
            groups.append({
                "label": model._meta.verbose_name_plural,
                "items": [{"obj": obj, "ct_id": ct_id} for obj in objects],
            })
    return groups


def _trash_object(contentTypeId, objectId):
    from django.contrib.contenttypes.models import ContentType
    from django.shortcuts import get_object_or_404

    content_type = get_object_or_404(ContentType, pk=contentTypeId)
    model = content_type.model_class()
    return model.objects.all_with_deleted().filter(pk=objectId).first()


@login_required(login_url='/accounts/login/')
@require_perm("trash.view_all")
def trash(request):
    return render(request, "hub/trash.html", {"groups": _deleted_groups()})


@login_required(login_url='/accounts/login/')
@require_perm("trash.restore_all")
def trashRestore(request, contentTypeId, objectId):
    from django.shortcuts import redirect

    obj = _trash_object(contentTypeId, objectId)
    if request.method == "POST" and obj is not None:
        obj.undelete()
    return redirect("trash")


@login_required(login_url='/accounts/login/')
@require_perm("trash.delete_forever_all")
def trashDeleteForever(request, contentTypeId, objectId):
    from django.shortcuts import redirect

    obj = _trash_object(contentTypeId, objectId)
    if request.method == "POST" and obj is not None:
        obj.delete()
    return redirect("trash")


@login_required(login_url='/accounts/login/')
def emailPreferences(request):
    """Per-category email opt-out (§6) and language (§14)."""
    from django.conf import settings as django_settings

    from hub.mail import is_subscribed, set_subscription
    from hub.models import EmailPreference
    from organisation.models import (
        DETAIL_LAYOUT_CHOICES,
        LIST_VIEW_CHOICES,
        SIDEBAR_POSITION_CHOICES,
        VIEW_MODE_CHOICES,
        UserProfile,
    )
    from organisation.services import active_organisation

    categories = EmailPreference.CATEGORY_CHOICES
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user, organisation=active_organisation(request)
    )
    if request.method == "POST":
        for value, _label in categories:
            set_subscription(request.user, value, request.POST.get(value) == "on")
        language = request.POST.get("language", "")
        if language in dict(django_settings.LANGUAGES):
            profile.language = language
        for field in ("sidebar_position_desktop", "sidebar_position_mobile", "view_mode",
                      "list_view_desktop", "list_view_mobile", "detail_layout_desktop"):
            value = request.POST.get(field, "")
            if value in dict(UserProfile._meta.get_field(field).choices):
                setattr(profile, field, value)
        for field in ("icon_size_desktop", "icon_size_mobile", "text_size_desktop", "text_size_mobile"):
            value = request.POST.get(field, "")
            if value.isdigit():
                setattr(profile, field, int(value))
        for field in ("sound_enabled", "vibration_enabled", "image_on_scan"):
            setattr(profile, field, request.POST.get(field) == "on")
        volume = request.POST.get("volume", "")
        if volume.isdigit():
            profile.volume = int(volume)
        profile.save()
        return redirect("email preferences")
    return render(request, "hub/emailPreferences.html", {
        "categories": [
            {"value": value, "label": label, "subscribed": is_subscribed(request.user, value)}
            for value, label in categories
        ],
        "languages": django_settings.LANGUAGES,
        "current_language": profile.language,
        "profile": profile,
        "sidebar_positions": SIDEBAR_POSITION_CHOICES,
        "view_modes": VIEW_MODE_CHOICES,
        "list_views": LIST_VIEW_CHOICES,
        "detail_layouts": DETAIL_LAYOUT_CHOICES,
    })


@login_required(login_url='/accounts/login/')
def saveDefaultColumns(request):
    """Save the current column selection as the user's default (§ list-views)."""
    if request.method == "POST":
        from organisation.services import active_profile

        list_type = request.POST.get("list_type", "")
        profile = active_profile(request)
        if profile is not None and list_type:
            cols = [c for c in request.POST.get("cols", "").split(",") if c]
            profile.list_columns = {**(profile.list_columns or {}), list_type: cols}
            profile.save()
    return redirect(request.POST.get("next") or "hub")

