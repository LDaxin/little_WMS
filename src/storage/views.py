from django.utils.translation import gettext as _
from hub.toasts import toast
from hub.csv import csv_response
from hub.search import filter_by_search
from hub.columns import default_columns, order_by, selected_columns
from hub.columns import columns as all_columns
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.urls import reverse
from .forms import *
from .models import *
from codeSystem.models import *
from article.models import Article, Stock
from article.views import composition_context, composition_warning
from tag.models import Tag
from movement.services import MovementService
from django.contrib.auth.decorators import login_required
from organisation.decorators import require_perm
from organisation.services import active_profile
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
import json
from time import sleep

PAGE_SIZE = 50

@login_required(login_url='/accounts/login/')
@require_perm("storage.view_all")
def storage(request, typ, storageId):
        storageObject = Storage.objects.get(pk=storageId)

        if storageObject.typ.name == typ:
            instancedStorageForum = FormChangeStorage(instance=storageObject)
            context = {
                "symbol":storageObject.typ.symbol,
                "searchFieldName":"storageSearch" + storageObject.typ.name,
                "modalId":"single",
                "form":[instancedStorageForum],
                "typ":typ,
                "actionType":"update",
                "id":storageId,
                "code":storageObject.code.code if storageObject.code else "",
                "link":("/s/" + storageObject.code.code) if storageObject.code else "",
                "storageContents":True,
                "contents":Stock.objects.filter(stored=storageObject.space),
                "storeUrl":"./%s/store" % storageId,
                "removeUrl":"./%s/remove" % storageId,
                "tagChips":True,
                "tags":storageObject.tags.all(),
                "allTags":Tag.objects.all(),
                "tagAddUrl":"./%s/tags/add" % storageId,
                "tagRemoveUrl":"./%s/tags/remove" % storageId,
                "imageGallery":True,
                "images":storageObject.images.all(),
                "imageBaseUrl":"./%s/images/" % storageId,
                "floorPlanUrl":"./%s/plan" % storageId,
            }
            context.update(composition_context(storageObject.space))
            return render(request, "hub/modules/item.html", context=context)
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + storageObject.typ.name)


@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def addStorageImage(request, typ, storageId):
    """Upload an image to a storage (§15)."""
    storage = Storage.objects.get(pk=storageId)
    if request.method == "POST" and request.FILES.get("image"):
        StorageImage.objects.create(
            storage=storage,
            image=request.FILES["image"],
            caption=request.POST.get("caption", ""),
            is_primary=not storage.images.exists(),
        )
    return redirect("storage", typ=typ, storageId=storageId)


@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def deleteStorageImage(request, typ, storageId, imageId):
    storage = Storage.objects.get(pk=storageId)
    if request.method == "POST":
        image = storage.images.filter(pk=imageId).first()
        if image:
            image.delete()
    return redirect("storage", typ=typ, storageId=storageId)


@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def setPrimaryStorageImage(request, typ, storageId, imageId):
    storage = Storage.objects.get(pk=storageId)
    if request.method == "POST":
        storage.images.update(is_primary=False)
        storage.images.filter(pk=imageId).update(is_primary=True)
    return redirect("storage", typ=typ, storageId=storageId)


def _plan_areas_json(plan):
    return [
        {
            "x": area.shape.get("x", 0),
            "y": area.shape.get("y", 0),
            "w": area.shape.get("w", 0),
            "h": area.shape.get("h", 0),
            "storage": area.storage_id or "",
            "label": area.label,
            "color": area.color,
        }
        for area in plan.areas.all()
    ]


def _plan_areas_px(plan):
    """Areas with pixel coordinates and a click target for the plan image.

    The target is the linked storage's own plan when it has one, otherwise its
    detail page.
    """
    if not plan.image:
        return []
    width, height = plan.image.width, plan.image.height
    storage_ids_with_plan = set(
        FloorPlan.objects.exclude(image="")
        .filter(image__isnull=False)
        .values_list("storage_id", flat=True)
    )
    areas = []
    for area in plan.areas.select_related("storage__typ"):
        storage = area.storage
        if storage is None:
            href = ""
        elif storage.pk in storage_ids_with_plan:
            href = reverse("floor plan", args=[storage.typ.name, storage.pk])
        else:
            href = reverse("storage", args=[storage.typ.name, storage.pk])
        areas.append({
            "storage": storage,
            "label": area.label,
            "color": area.color,
            "x": area.shape.get("x", 0) * width,
            "y": area.shape.get("y", 0) * height,
            "w": area.shape.get("w", 0) * width,
            "h": area.shape.get("h", 0) * height,
            "href": href,
        })
    return areas


@login_required(login_url='/accounts/login/')
@require_perm("storage.view_all")
def floorPlan(request, typ, storageId):
    """Show a storage's floor plan with its clickable areas (§15)."""
    storage = Storage.objects.get(pk=storageId)
    plan, _ = FloorPlan.objects.get_or_create(storage=storage)
    highlight = request.GET.get("highlight", "")
    return render(request, "hub/modules/floorPlan.html", {
        "plan": plan,
        "areas": _plan_areas_px(plan),
        "highlight": int(highlight) if highlight.isdigit() else None,
    })


@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def floorPlanEdit(request, typ, storageId):
    """Draw areas on a storage's floor plan (§15)."""
    storage = Storage.objects.get(pk=storageId)
    plan, _ = FloorPlan.objects.get_or_create(storage=storage)
    return render(request, "hub/modules/floorPlanEditor.html", {
        "plan": plan,
        "areas": _plan_areas_json(plan),
        "storages": [{"id": s.id, "name": str(s)} for s in Storage.objects.all()],
    })


@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def uploadFloorPlan(request, typ, storageId):
    """Upload or replace a storage's floor plan image (§15, Stage 1)."""
    storage = Storage.objects.get(pk=storageId)
    plan, _ = FloorPlan.objects.get_or_create(storage=storage)
    if request.method == "POST" and request.FILES.get("image"):
        plan.image = _resize_plan_upload(request.FILES["image"])
        plan.save()
    return redirect("edit floor plan", typ=typ, storageId=storageId)


def _resize_plan_upload(upload, max_edge=2000):
    """Scale a plan image down so the SVG stays light in the browser."""
    from io import BytesIO

    from django.core.files.base import ContentFile
    from PIL import Image, ImageOps

    img = ImageOps.exif_transpose(Image.open(upload)).convert("RGB")
    if max(img.size) > max_edge:
        img.thumbnail((max_edge, max_edge))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return ContentFile(buf.getvalue(), name=upload.name)


@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def saveFloorPlanAreas(request, typ, storageId):
    """Replace a floor plan's areas with the drawn ones (§15, Stage 2)."""
    storage = Storage.objects.get(pk=storageId)
    plan, _ = FloorPlan.objects.get_or_create(storage=storage)
    if request.method == "POST":
        try:
            areas = json.loads(request.POST.get("areas", "[]"))
        except ValueError:
            areas = []
        plan.areas.all().delete()
        for area in areas:
            storage_id = area.get("storage")
            FloorPlanArea.objects.create(
                floor_plan=plan,
                storage_id=int(storage_id) if str(storage_id).isdigit() else None,
                shape={
                    "x": area.get("x", 0),
                    "y": area.get("y", 0),
                    "w": area.get("w", 0),
                    "h": area.get("h", 0),
                },
                label=area.get("label", ""),
                color=area.get("color", "#0d6efd"),
            )
    return redirect("floor plan", typ=typ, storageId=storageId)
    

@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def storageIncert(request, typ, storageId):
    try:
        storageObject = Storage.objects.get(pk=storageId)
        if storageObject.typ.name == typ:
            instancedStorageForum = FormChangeStorage(instance=storageObject)
            context = {
                "symbol":storageObject.typ.symbol,
                "searchFieldName":"storageSearch" + storageObject.typ.name,
                "modalId":"single",
                "form":[instancedStorageForum],
                "typ":typ,
                "actionType":"update",
                "id":storageId
            }
            return render(request, "hub/modules/itemForm.html", context=context)
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + storageObject.typ.name)
    
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
@require_perm("storage.view_all")
def storages(request, typ):

    storageTypeObject = StorageType.objects.get(name__exact=typ)

    if storageTypeObject == None:
         return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        context = {
            "symbol":storageTypeObject.symbol,
            "searchFieldName":"storageSearch" + storageTypeObject.name,
            'type':"storage",
            "list_type":"storage",
            "available_columns": all_columns("storage"),
            "columns": selected_columns("storage", request.GET.get("cols"), active_profile(request)),
            "cols": request.GET.get("cols", ""),
            "sort": request.GET.get("sort", ""),
            "name":typ,
            "form":[FormStorage()],
            "typ":typ,
            "add":True,
            "del":True,
            "export":True,
            "qr":True
        }
        return render(request, "hub/modules/items.html", context=context)


@login_required(login_url='/accounts/login/')
@require_perm("storage.view_all")
def storagesAll(request):
    """List all storages across types."""
    return render(request, "hub/modules/items.html", context={
        "symbol": "Logo",
        "searchFieldName": "storageSearchAll",
        "type": "storage",
        "list_type": "storage",
        "available_columns": all_columns("storage"),
        "columns": selected_columns("storage", request.GET.get("cols"), active_profile(request)),
        "cols": request.GET.get("cols", ""),
        "sort": request.GET.get("sort", ""),
        "name": "",
        "form": [],
        "typ": "",
        "show_type": True,
        "add": False,
        "del": False,
        "export": False,
        "qr": False,
    })


@login_required(login_url='/accounts/login/')
@require_perm("storage.view_all")
def searchStoragesAll(request):
    if request.method == "GET":
        r = filter_by_search(
            Storage.objects.select_related("typ").prefetch_related("images"),
            request.GET.get("search", ""), "name", "code__code",
        )
        sort = request.GET.get("sort", "")
        r = order_by(r, "storage", sort)
        page = Paginator(r, PAGE_SIZE).get_page(request.GET.get("page"))
        cols = request.GET.get("cols", "")
        template = "hub/modules/listAppend.html" if request.GET.get("append") else "hub/modules/list.html"
        return render(request, template, context={
            "list_type": "storage",
            "columns": selected_columns("storage", cols, active_profile(request)),
            "rows": page.object_list,
            "selectable": True,
            "sort": sort,
            "cols": cols,
            "searchFieldName": "storageSearchAll",
            "page": page,
        })


@login_required(login_url='/accounts/login/')
@require_perm("storage.create_all")
def addModal(request, typ):
    context = {
        "modalId":"add",
        "form":[FormStorage()],
        "actionType":"add",
    }
    return render(request, "hub/modules/addForm.html", context=context)

@login_required(login_url='/accounts/login/')
@require_perm("storage.delete_all")
def delModal(request, typ):
    context = {
        "modalId":"del",
        "form":[FormStorage()],
        "actionType":"del",
    }
    return render(request, "hub/modules/delForm.html", context=context)

@login_required(login_url='/accounts/login/')
@require_perm("storage.create_all")
def addStorage(request, typ):

    t = StorageType.objects.get(name__exact=typ)

    if request.method == "POST":
        s = FormStorage(request.POST)
        if s.is_valid():
            storage = s.save(commit=False)
            storage.typ = t
            if s["code"].value().startswith("s0"):
                try:
                    code = UuidCode.objects.get(code=s["code"].value())
                    if code.used:
                        return toast(request, _("Error"), _("code is already used"), "alert")
                    code.used = True
                    code.save()
                    storage.code = code
                except:
                    return toast(request, _("Error"), _("not valid code"), "alert")
            else:
                pass

            so = storage.save()
            return toast(request, "Add Succses", str(storage) + " was added to your system.", "status", template="hub/modules/itemAdd.html")
        return toast(request, _("Error"), _("something went wrong"), "alert")
    return toast(request, _("Error"), _("something went wrong"), "alert")

@login_required(login_url='/accounts/login/')
@require_perm("storage.delete_all")
def delStorage(request, typ):
    if request.method == "POST":
        delList = []
        delListReturn = ""
        childList = []
        for key, value in request.POST.items():
            if key[0:1] == '_':
                try:
                    pa = Storage.objects.filter(pk=value).first()
                    ch = Storage.objects.filter(parent__pk=value)
                    delListReturn = delListReturn + pa.__str__() + ", "
                    for i in ch:
                        i.parent = None
                        i.save()
                    pa.delete()
                except Exception as e:
                    return toast(request, "Error", e, "alert")

        return toast(request, "Delete", delListReturn, "status", template="hub/modules/itemDelete.html")
    return toast(request, _("Error"), _("something went wrong"), "alert")

@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def updateStorage(request, storageId, typ):
    storageObject = Storage.objects.get(pk=storageId)

    if request.method == "POST":
        form = FormChangeStorage(request.POST, instance=storageObject)
        if form.is_valid():
            form.save()
            return toast(request, "Update", str(storageObject) + " was updated", "status")
        return toast(request, _("Error"), _("something went wrong"), "alert")


def _storage_contents_context(storage, storeUrl, removeUrl, error="", warning="", forceCode=""):
    return {
        "contents": Stock.objects.filter(stored=storage.space).select_related("article__base"),
        "storeUrl": storeUrl,
        "removeUrl": removeUrl,
        "storeSearchUrl": storeUrl + "-search",
        "storeError": error,
        "storeWarning": warning,
        "forceCode": forceCode,
    }


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def storeInStorage(request, typ, storageId):
    storage = Storage.objects.get(pk=storageId)
    storeUrl = "./%s/store" % storageId
    removeUrl = "./%s/remove" % storageId
    if request.method == "POST":
        code = request.POST.get("code", "")
        try:
            article = Article.objects.get(code__code=code)
            warning = composition_warning(storage.space, article)
            if warning and not request.POST.get("force"):
                return render(request, "hub/modules/storageContents.html",
                              context=_storage_contents_context(storage, storeUrl, removeUrl,
                                                                warning=warning, forceCode=code))
            amount = request.POST.get("amount", "").strip()
            amount = int(amount) if amount.isdigit() else None
            MovementService.store_article(article, storage.space, request.user, amount=amount)
            error = ""
        except Article.DoesNotExist:
            error = "No article with that code"
        except ValidationError as e:
            error = e.messages[0] if e.messages else str(e)
        return render(request, "hub/modules/storageContents.html",
                      context=_storage_contents_context(storage, storeUrl, removeUrl, error))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def storeArticleSearch(request, typ, storageId):
    """Live suggestions for the store-article field (code or name, § code-input)."""
    query = request.GET.get("code", "").strip()
    if query:
        articles = filter_by_search(Article.objects.all(), query, "base__name", "code__code")[:20]
    else:
        articles = Article.objects.none()
    return render(request, "hub/modules/storeArticleResults.html", {
        "articles": articles,
        "storeUrl": "./%s/store" % storageId,
    })


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def removeFromStorage(request, typ, storageId, articleId):
    storage = Storage.objects.get(pk=storageId)
    storeUrl = "./%s/store" % storageId
    removeUrl = "./%s/remove" % storageId
    if request.method == "POST":
        article = Article.objects.get(pk=articleId)
        MovementService.remove_article(article, space=storage.space, user=request.user)
        return render(request, "hub/modules/storageContents.html",
                      context=_storage_contents_context(storage, storeUrl, removeUrl))
    return HttpResponseNotFound('<h1>Page not found</h1>')


def _tag_chips_context(obj, tagAddUrl, tagRemoveUrl, error=""):
    return {
        "tags": obj.tags.all(),
        "allTags": Tag.objects.all(),
        "tagAddUrl": tagAddUrl,
        "tagRemoveUrl": tagRemoveUrl,
        "tagError": error,
    }


@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def addStorageTag(request, typ, storageId):
    storage = Storage.objects.get(pk=storageId)
    tagAddUrl = "./%s/tags/add" % storageId
    tagRemoveUrl = "./%s/tags/remove" % storageId
    if request.method == "POST":
        name = request.POST.get("tag", "").strip()
        tag = Tag.objects.filter(name__iexact=name).first()
        if tag is None:
            error = "No tag named %s" % name
        else:
            storage.tags.add(tag)
            error = ""
        return render(request, "hub/modules/tagChips.html",
                      context=_tag_chips_context(storage, tagAddUrl, tagRemoveUrl, error))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def removeStorageTag(request, typ, storageId, tagId):
    storage = Storage.objects.get(pk=storageId)
    tagAddUrl = "./%s/tags/add" % storageId
    tagRemoveUrl = "./%s/tags/remove" % storageId
    if request.method == "POST":
        storage.tags.remove(Tag.objects.get(pk=tagId))
        return render(request, "hub/modules/tagChips.html",
                      context=_tag_chips_context(storage, tagAddUrl, tagRemoveUrl))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
@require_perm("storage.view_all")
def searchStorages(request, typ):
    if request.method == "GET":
        r = filter_by_search(
            Storage.objects.filter(typ__name__exact=typ).select_related("typ").prefetch_related("images"),
            request.GET.get("search", ""), "name", "code__code",
        )
        sort = request.GET.get("sort", "")
        r = order_by(r, "storage", sort)
        page = Paginator(r, PAGE_SIZE).get_page(request.GET.get("page"))
        cols = request.GET.get("cols", "")
        template = "hub/modules/listAppend.html" if request.GET.get("append") else "hub/modules/list.html"
        return render(request, template, context={
            "list_type": "storage",
            "columns": selected_columns("storage", cols, active_profile(request)),
            "rows": page.object_list,
            "selectable": True,
            "sort": sort,
            "cols": cols,
            "searchFieldName": "storageSearch" + typ,
            "page": page,
        })


@login_required(login_url='/accounts/login/')
@require_perm("export.csv_all")
def exportStorages(request, typ):
    rows = []
    for key, value in request.POST.items():
        if key.startswith("_"):
            storage = Storage.objects.get(pk=value)
            if storage.typ.name == typ:
                rows.append([storage.name, storage.code.code, storage.typ.name])
    return csv_response("storages.csv", ["name", "code", "type"], rows, encoding="iso-8859-1")

@login_required(login_url='/accounts/login/')
@require_perm("storage.view_all")
def storageScanner(request, typ, scannerId, state):
    if state == "toggle":
        print(request.POST)
        if request.POST["active_scanner"] == scannerId:
            context = {
                "activeInput":"",
                "input":scannerId,
                "state":"off",
            }
            return render(request, "hub/modules/toggleScanner.html", context=context)
        elif request.POST["active_scanner"] == "":
            context = {
                "activeInput":"",
                "input":scannerId,
                "state":"on",
            }
        else:
            context = {
                "activeInput":request.POST["active_scanner"],
                "input":scannerId,
                "state":"on",
            }
        return render(request, "hub/modules/toggleScanner.html", context=context)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
