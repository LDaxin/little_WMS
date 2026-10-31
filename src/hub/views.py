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

