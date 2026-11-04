from django.utils.translation import gettext as _
from hub.toasts import toast
from hub.search import filter_by_search
from hub.columns import is_mobile, resolve_detail_layout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from organisation.decorators import require_perm
from .models import *
from .forms import *

# Create your views here.

@login_required(login_url='/accounts/login/')
@require_perm("tag.view_all")
def tag(request, tagId):
    try:
        tagObject = Tag.objects.get(pk=tagId)
        tagForm = FormChangeTag(instance=tagObject)
        detailUrl = "/tag/%s" % tagId
        context = {
            "symbol": "Tag",
            "searchFieldName": "tagSearch",
            "id": tagId,
            "modalId": "single",
            "form": [tagForm],
            "actionType": "update",
            "updateUrl": "/tag/%s/update" % tagId,
            "detailUrl": detailUrl,
            "editUrl": detailUrl + "/i",
            "readUrl": detailUrl + "?fields=read",
            "detailHeader": {
                "name": tagObject.name,
                "code": "",
                "type": _("Tag"),
                "image": None,
                "link": "",
                "store": False,
            },
        }
        context["detailLayout"] = resolve_detail_layout(request)
        context["detailLayoutSwitchable"] = not is_mobile(request)
        context["detailSections"] = []
        if request.GET.get("fields") == "read":
            return render(request, "hub/modules/itemSummary.html", context=context)
        if request.GET.get("fields") == "sections":
            return render(request, "hub/modules/itemSections.html", context=context)
        template = "hub/modules/itemModal.html" if request.headers.get("HX-Request") else "hub/modules/item.html"
        return render(request, template, context=context)
    except Tag.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    

@login_required(login_url='/accounts/login/')
@require_perm("tag.edit_all")
def tagIncert(request, tagId):
    try:
        tagObject = Tag.objects.get(pk=tagId)
        tagForm = FormChangeTag(instance=tagObject)
        detailUrl = "/tag/%s" % tagId
        context = {
            "searchFieldName": "tagSearch",
            "id": tagId,
            "modalId": "single",
            "form": [tagForm],
            "actionType": "update",
            "updateUrl": "/tag/%s/update" % tagId,
            "readUrl": detailUrl + "?fields=read",
        }
        return render(request, "hub/modules/itemForm.html", context=context)
    except Tag.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
@require_perm("tag.view_all")
def tags(request):
    return render(request, "hub/modules/items.html", context={"symbol":"Tag", "searchFieldName":"tagSearch", 'type':"tag", "name":"tag", "form":[FormTag], "modalId":"add"})

@login_required(login_url='/accounts/login/')
@require_perm("tag.create_all")
def addTag(request):
    if request.method == "POST":
        tagForm = FormTag(request.POST)
        if tagForm.is_valid():
            tag = tagForm.save()
            tag.save()
            return toast(request, "Add Succses", str(tag) + " was added to your system.", "status")

@login_required(login_url='/accounts/login/')
@require_perm("tag.delete_all")
def delTag(request):
    if request.method == "POST":
        delList = []
        delListReturn = ""
        for key, value in request.POST.items():
            if key[0:1] == '_':
                try:
                    pa = Tag.objects.filter(pk=value).first()
                    delList.append(pa)
                except Exception as e:
                    return toast(request, "Error", e, "alert")
        for i in delList:
            delListReturn = delListReturn + i.__str__() + " "
            i.deleted = True
            i.save()
        return toast(request, "Delete", delListReturn, "alert")
    return toast(request, _("Error"), _("thomething went wrong"), "alert")






@login_required(login_url='/accounts/login/')
@require_perm("tag.edit_all")
def updateTag(request, tagId):
    tagObject = Tag.objects.get(pk=tagId)

    if request.method == "POST":
        tagForm = FormTag(request.POST, instance=tagObject)
        if tagForm.is_valid():
            tagForm.save()
            response = toast(request, _("Update Succses"), _("Tag was updated."), "status")
            response["HX-Trigger"] = "detail-updated"
            return response

@login_required(login_url='/accounts/login/')
@require_perm("tag.view_all")
def searchTags(request):
    if request.method == "GET":
        r = filter_by_search(Tag.objects.all(), request.GET.get("search", ""), "name", "code__code")
        return render(request, "hub/modules/results.html", context={"results": r, "type": "tag"})
