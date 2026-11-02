from django.utils.translation import gettext as _
from hub.toasts import toast
from hub.search import filter_by_search
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
        return render(request, "hub/modules/item.html", context={"symbol":"Tag", "searchFieldName":"tagSearch", "id":tagId, "modalId":"single", "form":[tagForm], "actionType":"update"})
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    

@login_required(login_url='/accounts/login/')
@require_perm("tag.edit_all")
def tagIncert(request, tagId):
    try:
        tagObject = Tag.objects.get(pk=tagId)
        tagForm = FormChangeTag(instance=tagObject)
        return render(request, "hub/modules/itemForm.html", context={"searchFieldName":"tagSearch",  "id":tagId, "modalId":"single", "form":[tagForm], "actionType":"update"})
    except:
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
            return toast(request, _("Update Succses"), _("Tag was updated."), "status")

@login_required(login_url='/accounts/login/')
@require_perm("tag.view_all")
def searchTags(request):
    if request.method == "GET":
        r = filter_by_search(Tag.objects.all(), request.GET.get("search", ""), "name", "code__code")
        return render(request, "hub/modules/results.html", context={"results": r, "type": "tag"})
