from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.

@login_required(login_url='/accounts/login/')
def locations(request):
    return render(request, "hub/modules/items.html", context={"list":Location.objects.all(), "type":"location", "form":[Form_location]})

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
        l = Form_location(request.POST)
        if l.is_valid():
            location = l.save()
            location.save()
            return render(request, "hub/modules/toast.html", context={"toastName":"Add Succses", "toastId":"successToast", "toastText":str(location) + " was added to your system.", "toastType":"status"})
    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"thomething went wrong", "toastType":"alert"})

