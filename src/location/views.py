from django.utils.translation import gettext as _
from hub.toasts import toast
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.contrib.auth.decorators import login_required
from organisation.decorators import require_perm
from .forms import *
from django.db.models import Q

# Create your views here.

@login_required(login_url='/accounts/login/')
@require_perm("location.view_all")
def location(request, locationId):
    try:
        locationObject = Location.objects.get(pk=locationId)
        locationForm = FormLocation(instance=locationObject)
        return render(request, "hub/modules/item.html", context={"symbol":"Location", "id":locationId, "searchFieldName":"locationSearch", "modalId":"single", "form":[locationForm], "actionType":"update", "code":locationObject.code.code if locationObject.code else "", "link":("/l/" + locationObject.code.code) if locationObject.code else ""})
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
@require_perm("location.edit_all")
def locationIncert(request, locationId):
    try:
        locationObject = Location.objects.get(pk=locationId)
        locationForm = FormLocation(instance=locationObject)
        return render(request, "hub/modules/itemForm.html", context={"symbol":"Location", "id":locationId, "searchFieldName":"locationSearch", "modalId":"single", "form":[locationForm], "actionType":"update"})
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
@require_perm("location.view_all")
def locations(request):
    return render(request, "hub/modules/items.html", context={"symbol":"Location", 'searchFieldName':"locationSearch", "modalId":"single", "name":"location", "type":"location", "form":[FormLocation]})

@login_required(login_url='/accounts/login/')
@require_perm("location.view_all")
def locationMap(request):
    locations = Location.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
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
            return toast(request, _("Update Succses"), _("Location was updated"), "status")
        return toast(request, _("Error"), _("thething went wrong"), "alert")

@login_required(login_url='/accounts/login/')
@require_perm("location.view_all")
def searchLocations(request):
    if request.method == "GET":
        search = request.GET.get("search", "")
        if search == "":
            r = Location.objects.all()
        else:
            r = Location.objects.filter(
                Q(line1__contains=search) | Q(city__contains=search) | Q(code__code__contains=search)
            )
        return render(request, "hub/modules/results.html", context={"results":r, "type":"location"})
