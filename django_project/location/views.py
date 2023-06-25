from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.

@login_required(login_url='/accounts/login/')
def location(request, locationId):
    try:
        locationObject = Location.objects.get(pk=locationId)
        locationForm = FormLocation(instance=locationObject)
        return render(request, "hub/modules/item.html", context={"symbol":"Location", "id":locationId, "searchFieldName":"locationSearch", "modalId":"single", "form":[locationForm], "actionType":"update"})
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
def locationIncert(request, locationId):
    try:
        locationObject = Location.objects.get(pk=locationId)
        locationForm = FormLocation(instance=locationObject)
        return render(request, "hub/modules/itemForm.html", context={"symbol":"Location", "id":locationId, "searchFieldName":"locationSearch", "modalId":"single", "form":[locationForm], "actionType":"update"})
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
def locations(request):
    return render(request, "hub/modules/items.html", context={"symbol":"Location", 'searchFieldName':"locationSearch", "modalId":"single", "name":"location", "type":"location", "form":[FormLocation]})

@login_required(login_url='/accounts/login/')
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
                    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":e, "toastType":"alert"})
        for i in delList:
            delListReturn = delListReturn + i.__str__() + " "
            i.deleted = True
            i.save()
        return render(request, "hub/modules/toast.html", context={"toastName":"Delete", "toastId":"successToast", "toastText":delListReturn, "toastType":"alert"})
    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"thomething went wrong", "toastType":"alert"})


@login_required(login_url='/accounts/login/')
def addLocation(request):
    if request.method == "POST":
        l = FormLocation(request.POST)
        if l.is_valid():
            location = l.save()
            location.save()
            return render(request, "hub/modules/toast.html", context={"toastName":"Add Succses", "toastId":"successToast", "toastText":str(location) + " was added to your system.", "toastType":"status"})
    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"thomething went wrong", "toastType":"alert"})

@login_required(login_url='/accounts/login/')
def updateLocation(request, locationId):
    locationObject = Location.objects.get(pk=locationId)
    
    if request.method == "POST":
        locationForm = FormLocation(request.POST, instance=locationObject)
        if locationForm.is_valid():
            locationForm.save()
            return render(request, "hub/modules/toast.html", context={"toastName":"Update Succses", "toastId":"successToast", "toastText":"Location was updated", "toastType":"status"})
        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"thething went wrong", "toastType":"alert"})
