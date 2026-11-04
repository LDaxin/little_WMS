from django.utils.translation import gettext as _
from hub.toasts import toast
from hub.search import filter_by_search
from hub.columns import is_mobile, resolve_detail_layout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.contrib.auth.decorators import login_required
from organisation.decorators import require_perm
from .forms import *

# Create your views here.

@login_required(login_url='/accounts/login/')
@require_perm("location.view_all")
def location(request, locationId):
    try:
        locationObject = Location.objects.get(pk=locationId)
        locationForm = FormLocation(instance=locationObject)
        detailUrl = "/location/%s" % locationId
        linkedStorages = locationObject.storage_set.all()
        linkedOccasions = locationObject.occasion_set.all()
        context = {
            "symbol": "Location",
            "id": locationId,
            "searchFieldName": "locationSearch",
            "modalId": "single",
            "form": [locationForm],
            "actionType": "update",
            "updateUrl": "/location/%s/update" % locationId,
            "code": locationObject.code.code if locationObject.code else "",
            "link": ("/l/" + locationObject.code.code) if locationObject.code else "",
            "linkedStorages": linkedStorages,
            "linkedOccasions": linkedOccasions,
            "detailUrl": detailUrl,
            "editUrl": detailUrl + "/i",
            "readUrl": detailUrl + "?fields=read",
            "detailHeader": {
                "name": str(locationObject),
                "code": locationObject.code.code if locationObject.code else "",
                "type": _("Location"),
                "image": None,
                "link": ("/l/" + locationObject.code.code) if locationObject.code else "",
                "store": False,
            },
        }
        context["detailLayout"] = resolve_detail_layout(request)
        context["detailLayoutSwitchable"] = not is_mobile(request)
        context["detailSections"] = _location_sections(linkedStorages, linkedOccasions)
        if request.GET.get("fields") == "read":
            return render(request, "hub/modules/itemSummary.html", context=context)
        if request.GET.get("fields") == "sections":
            return render(request, "hub/modules/itemSections.html", context=context)
        template = "hub/modules/itemModal.html" if request.headers.get("HX-Request") else "hub/modules/item.html"
        return render(request, template, context=context)
    except Location.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def _location_sections(linkedStorages, linkedOccasions):
    """The collapsible detail sections for a location (§ detail-view)."""
    sections = []
    count = len(linkedStorages) + len(linkedOccasions)
    if count:
        sections.append({"key": "linked", "label": _("Linked objects"),
                         "count": count,
                         "template": "location/linkedObjects.html"})
    return sections


@login_required(login_url='/accounts/login/')
@require_perm("location.edit_all")
def locationIncert(request, locationId):
    try:
        locationObject = Location.objects.get(pk=locationId)
        locationForm = FormLocation(instance=locationObject)
        detailUrl = "/location/%s" % locationId
        context = {
            "symbol": "Location",
            "id": locationId,
            "searchFieldName": "locationSearch",
            "modalId": "single",
            "form": [locationForm],
            "actionType": "update",
            "updateUrl": "/location/%s/update" % locationId,
            "readUrl": detailUrl + "?fields=read",
            "mapPicker": True,
        }
        return render(request, "hub/modules/itemForm.html", context=context)
    except Location.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
@require_perm("location.view_all")
def locations(request):
    return render(request, "hub/modules/items.html", context={"symbol":"Location", 'searchFieldName':"locationSearch", "modalId":"single", "name":"location", "type":"location", "form":[FormLocation], "add":True, "del":True})

@login_required(login_url='/accounts/login/')
@require_perm("location.view_all")
def locationMap(request):
    locations = (
        Location.objects.exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .prefetch_related("storage_set", "occasion_set")
    )
    return render(request, "location/map.html", context={"locations": locations})

@login_required(login_url='/accounts/login/')
@require_perm("location.create_all")
def addLocation(request):
    if request.method == "POST":
        l = FormLocation(request.POST)
        if l.is_valid():
            location = l.save()
            location.save()
            return toast(request, "Add Succses", str(location) + " was added to your system.", "status")
    return toast(request, _("Error"), _("thomething went wrong"), "alert")

@login_required(login_url='/accounts/login/')
@require_perm("location.delete_all")
def delLocation(request):
    if request.method == "POST":
        delList = []
        delListReturn = ""
        for key, value in request.POST.items():
            if key[0:1] == '_':
                try:
                    pa = Location.objects.filter(pk=value).first()
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
@require_perm("location.edit_all")
def updateLocation(request, locationId):
    locationObject = Location.objects.get(pk=locationId)
    
    if request.method == "POST":
        locationForm = FormLocation(request.POST, instance=locationObject)
        if locationForm.is_valid():
            locationForm.save()
            response = toast(request, _("Update Succses"), _("Location was updated"), "status")
            response["HX-Trigger"] = "detail-updated"
            return response
        return toast(request, _("Error"), _("thething went wrong"), "alert")

@login_required(login_url='/accounts/login/')
@require_perm("location.view_all")
def searchLocations(request):
    if request.method == "GET":
        r = filter_by_search(Location.objects.all(), request.GET.get("search", ""), "line1", "city", "code__code")
        return render(request, "hub/modules/results.html", context={"results": r, "type": "location"})
