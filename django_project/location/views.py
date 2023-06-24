from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.

@login_required(login_url='/accounts/login/')
def locations(request):
    return render(request, "hub/modules/items.html", context={"list":Location.objects.all(), "type":"location", "form":[FormLocation]})

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
def location(request, locationId):
    try:
        locationObject = Location.objects.get(pk=locationId)
        locationForm = FormLocation(instance=locationObject)
        return render(request, "hub/modules/itemForm.html", context={"symbol":"location", "form":[locationForm]})
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
def locationIncert(request, locationId):
    try:
        locationObject = Location.objects.get(pk=locationId)
        locationForm = FormLocation(instance=locationObject)
        return render(request, "hub/modules/itemForm.html", context={"symbol":"location", "form":[locationForm]})
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

