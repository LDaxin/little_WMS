from django.shortcuts import render
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

    import json

    organisation = active_organisation(request)
    context = {}

    if has_perm(request.user, "occasion.view_all", organisation):
        context["upcomingOccasions"] = Occasion.objects.filter(
            calendar_entry__start_date__gte=date.today()
        ).order_by("calendar_entry__start_date")[:5]

    if has_perm(request.user, "notification.view_all", organisation):
        context["unreadNotifications"] = request.user.notifications.filter(is_read=False)[:5]

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

    from querybuilder.services import ARTICLE_FIELDS, QueryError, parse_json
    from savedviews.models import SavedView

    widgets = []
    for view in SavedView.objects.filter(owner=request.user, show_on_dashboard=True):
        articles = Article.objects.all()
        try:
            articles = articles.filter(parse_json(json.dumps(view.query), ARTICLE_FIELDS))
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

